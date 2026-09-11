#!/usr/bin/env python3
"""Validate and produce an installable ZIP rooted at ric-design-patterns-skill/."""
import argparse, datetime, hashlib, json, subprocess, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','.bootstrap','__pycache__','.build','bin','obj','node_modules','dist'}

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',type=Path,default=ROOT.parent)
    args=p.parse_args(); subprocess.run([sys.executable,str(ROOT/'scripts/validate.py')],check=True)
    release=json.loads((ROOT/'data/release.json').read_text()); name=release['name']
    args.output.mkdir(parents=True,exist_ok=True); target=args.output/f"{name}-{release['version']}.zip"
    stamp=(*datetime.date.fromisoformat(release['date']).timetuple()[:3],0,0,0)
    files=[f for f in sorted(ROOT.rglob('*')) if f.is_file() and not any(part in EXCLUDED for part in f.relative_to(ROOT).parts) and f.suffix not in {'.pyc','.class','.jar','.zip','.gz','.xz'}]
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for f in files:
            info=zipfile.ZipInfo(name+'/'+str(f.relative_to(ROOT)),date_time=stamp); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
            archive.writestr(info,f.read_bytes())
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix(target.suffix+'.sha256').write_text(digest+'  '+target.name+'\n')
    print(f'{target}\n{len(files)} files; SHA-256 {digest}')
if __name__=='__main__': main()
