#!/usr/bin/env python3
"""Compile/run standalone examples; record only observed results with source hashes."""
from __future__ import annotations
import argparse, concurrent.futures, datetime, hashlib, json, os, platform, shutil, subprocess, sys, tempfile, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    'python': ['python3'], 'javascript': ['node'], 'typescript': ['tsc','node'],
    'java': ['javac','java'], 'cpp': ['g++'], 'go': ['go'], 'rust': ['rustc'],
    'php': ['php'], 'ruby': ['ruby'], 'swift': ['swiftc'], 'kotlin': ['kotlinc','java'], 'csharp': ['dotnet']}
VERSION_ARGS = {'java':['-version'], 'javac':['-version'], 'go':['version'], 'php':['--version'], 'kotlinc':['-version']}

def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

def call(args: list[str], cwd: Path, timeout: int = 120, stdin: str | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.update({'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','PYTHONDONTWRITEBYTECODE':'1'})
    return subprocess.run(args, cwd=cwd, input=stdin, text=True, capture_output=True, timeout=timeout, env=env)

def diagnostic(result, root: Path) -> str:
    return (result.stdout + result.stderr).strip().replace(str(root), '<temporary>')[-4000:]

def commands(language: str, source: Path, directory: Path) -> tuple[list[list[str]], list[str], str | None]:
    f = str(source)
    binary = str(directory/'demo')
    if language == 'python': return [], ['python3',f], None
    if language == 'javascript': return [], ['node',f], None
    if language == 'typescript':
        return [['tsc','--strict','--target','ES2022','--module','ES2022',f,'--outDir',str(directory/'js')]], ['node','--input-type=module'], 'generated-js'
    if language == 'java': return [['javac','--release','17','-d',str(directory),f]], ['java','-ea','-cp',str(directory),'Main'], None
    if language == 'cpp': return [['g++','-std=c++17','-Wall','-Wextra','-pedantic',f,'-o',binary]], [binary], None
    if language == 'go': return [], ['go','run',f], None
    if language == 'rust': return [['rustc','--edition=2021',f,'-o',binary]], [binary], None
    if language == 'php': return [], ['php',f], None
    if language == 'ruby': return [], ['ruby',f], None
    if language == 'swift': return [['swiftc','-swift-version','6',f,'-o',binary]], [binary], None
    if language == 'csharp':
        project = str(directory/'Example.csproj')
        return [['dotnet','build',project,'--configuration','Release','--nologo','--verbosity','quiet']], ['dotnet',str(directory/'bin/Release/net8.0/Example.dll')], None
    raise ValueError(f'Unsupported individual runner: {language}')

def one(language: str, slug: str, metadata: dict, bank: dict, missing: list[str], timeout: int) -> tuple[str,dict]:
    code = bank[slug]['code']
    result = {'sha256':hashlib.sha256(code.encode()).hexdigest(),'status':'skipped','checked_at':now()}
    if missing:
        result['diagnostic'] = 'Missing toolchains: '+', '.join(missing)
        return slug, result
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='ric-pattern-') as td:
        directory = Path(td)
        source = directory / metadata['file']
        source.write_text(code,encoding='utf-8')
        if language == 'csharp':
            project = ROOT/'examples'/language/slug/'Example.csproj'
            shutil.copyfile(project,directory/'Example.csproj')
            # There are no package dependencies; restore must not depend on external feeds.
            (directory/'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>')
        try:
            compile_commands, execute, stdin_mode = commands(language,source,directory)
            for command in compile_commands:
                completed = call(command,directory,timeout)
                if completed.returncode:
                    result.update(status='failed',phase='compile',returncode=completed.returncode,diagnostic=diagnostic(completed,directory))
                    return slug,result
            stdin = (directory/'js/main.js').read_text(encoding='utf-8') if stdin_mode else None
            completed = call(execute,directory,timeout,stdin)
            expected = 'OK '+slug
            passed = completed.returncode == 0 and completed.stdout.strip() == expected
            result.update(status='passed' if passed else 'failed',phase='run',returncode=completed.returncode,stdout=completed.stdout.strip(),duration_seconds=round(time.monotonic()-start,3))
            if not passed or completed.stderr.strip(): result['diagnostic'] = diagnostic(completed,directory)
        except (subprocess.TimeoutExpired, OSError, ValueError) as exc:
            result.update(status='failed',diagnostic=str(exc).replace(str(directory),'<temporary>'))
    return slug,result

def kotlin_batch(metadata: dict, bank: dict, missing: list[str], timeout: int) -> dict:
    results = {slug:{'sha256':hashlib.sha256(item['code'].encode()).hexdigest(),'status':'skipped','checked_at':now()} for slug,item in bank.items()}
    if missing:
        for r in results.values(): r['diagnostic']='Missing toolchains: '+', '.join(missing)
        return results
    with tempfile.TemporaryDirectory(prefix='ric-kotlin-') as td:
        directory=Path(td); files=[]
        for slug,item in bank.items():
            source=directory/slug/metadata['file']; source.parent.mkdir(); source.write_text(item['code'],encoding='utf-8'); files.append(str(source))
        jar=str(directory/'examples.jar')
        try:
            compiled=call(['kotlinc',*files,'-jvm-target','17','-include-runtime','-d',jar],directory,max(timeout,240))
            if compiled.returncode:
                for r in results.values(): r.update(status='failed',phase='compile',diagnostic=diagnostic(compiled,directory))
                return results
            for slug,r in results.items():
                executed=call(['java','-ea','-cp',jar,'patterns.'+slug.replace('-','_')+'.MainKt'],directory,timeout)
                r.update(status='passed' if executed.returncode==0 and executed.stdout.strip()=='OK '+slug else 'failed',phase='run',returncode=executed.returncode,stdout=executed.stdout.strip())
                if r['status']!='passed': r['diagnostic']=diagnostic(executed,directory)
        except (subprocess.TimeoutExpired,OSError) as exc:
            for r in results.values():
                if r['status']=='skipped': r.update(status='failed',diagnostic=str(exc).replace(str(directory),'<temporary>'))
    return results

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--languages',help='Comma-separated canonical language slugs; default: all')
    p.add_argument('--require-runtimes',action='store_true')
    p.add_argument('--record',default='data/verification.json')
    p.add_argument('--workers',type=int,default=2)
    p.add_argument('--timeout',type=int,default=120)
    args=p.parse_args()
    metadata={x['slug']:x for x in json.loads((ROOT/'data/languages.json').read_text())}
    selected=[s.strip() for s in args.languages.split(',')] if args.languages else list(metadata)
    if any(s not in metadata for s in selected): p.error('Unsupported language. Choices: '+', '.join(metadata))
    if args.workers<1 or args.timeout<1: p.error('workers and timeout must be positive')
    output=Path(args.record); output=output if output.is_absolute() else ROOT/output
    records=json.loads(output.read_text()) if output.exists() else {'schema_version':1,'languages':{}}
    failures=0
    for language in dict.fromkeys(selected):
        bank=json.loads((ROOT/'data/code'/f'{language}.json').read_text())
        missing=[tool for tool in TOOLS[language] if shutil.which(tool) is None]
        versions={}
        for tool in TOOLS[language]:
            if tool not in missing:
                try:
                    v=call([tool,*VERSION_ARGS.get(tool,['--version'])],ROOT,20)
                    versions[tool]=(v.stdout+v.stderr).strip().split('\n')[0][:300]
                except (OSError,subprocess.TimeoutExpired) as exc: versions[tool]='version query failed: '+type(exc).__name__
        if language=='kotlin': results=kotlin_batch(metadata[language],bank,missing,args.timeout)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures=[pool.submit(one,language,slug,metadata[language],bank,missing,args.timeout) for slug in bank]
                results=dict(f.result() for f in futures)
        records['languages'][language]={'environment':('GitHub Actions' if os.environ.get('GITHUB_ACTIONS') else 'Local')+' / '+platform.system()+' '+platform.machine(),'toolchains':versions,'examples':results}
        records['updated_at']=now()
        output.parent.mkdir(parents=True,exist_ok=True)
        temp=output.with_suffix(output.suffix+'.tmp'); temp.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); temp.replace(output)
        counts={status:sum(r['status']==status for r in results.values()) for status in ('passed','failed','skipped')}
        print(language+': '+json.dumps(counts),flush=True)
        for slug,r in results.items():
            if r['status']=='failed': print(f"  {slug}: {r.get('diagnostic','unexpected output')}",flush=True)
        failures+=counts['failed']+(counts['skipped'] if args.require_runtimes else 0)
    return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())
