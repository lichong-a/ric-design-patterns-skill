#!/usr/bin/env python3
"""Validate coverage, routing, generated source integrity and relative document links."""
from __future__ import annotations
import collections, hashlib, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit
from lookup import lookup
ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    errors=[]; warnings=[]
    def check(condition: bool, message: str) -> None:
        if not condition: errors.append(message)
    def read(path: str): return json.loads((ROOT/path).read_text(encoding='utf-8'))
    patterns=read('data/patterns.json'); languages=read('data/languages.json'); catalog=read('catalog.json')
    check(len(patterns)==23 and len(languages)==12,'Expected 23 patterns and 12 languages')
    check(collections.Counter(p['category'] for p in patterns)=={'creational':5,'structural':7,'behavioral':11},'Wrong GoF categories')
    check(len({p['slug'] for p in patterns})==23,'Duplicate pattern slugs')
    skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    check(skill.startswith('---\nname: ric-design-patterns-skill\n'),'Invalid Skill name/frontmatter')
    front=skill.split('---',2)[1]; description=re.search(r'^description: (.+)$',front,re.M)
    check(bool(description and 0<len(description.group(1))<=1024),'Missing or oversized description')
    check(len(skill.splitlines())<=80 and len(skill.encode())<=6000,'Entry is not lightweight')
    records=read('data/verification.json') if (ROOT/'data/verification.json').exists() else {'languages':{}}
    matched=0
    for language in languages:
        lang=language['slug']; bank=read(f'data/code/{lang}.json')
        check(set(bank)=={p['slug'] for p in patterns},f'Incomplete bank: {lang}')
        check((ROOT/f'references/{lang}/README.md').is_file(),f'Missing index: {lang}')
        for pattern in patterns:
            slug=pattern['slug']; code=bank[slug]['code']
            source=ROOT/f'examples/{lang}/{slug}'/language['file']; detail=ROOT/f'references/{lang}/{slug}.md'
            check(source.is_file() and detail.is_file(),f'Missing pair: {lang}/{slug}')
            if not source.is_file() or not detail.is_file(): continue
            check(source.read_text(encoding='utf-8')==code,f'Source drift: {source.relative_to(ROOT)}')
            text=detail.read_text(encoding='utf-8')
            check('```'+language['fence']+'\n'+code+'```' in text,f'Embedded code drift: {detail.relative_to(ROOT)}')
            check(catalog['languages'][lang]['patterns'][slug]==str(detail.relative_to(ROOT)),f'Wrong catalog path: {lang}/{slug}')
            record=records.get('languages',{}).get(lang,{}).get('examples',{}).get(slug,{})
            same=record.get('sha256')==hashlib.sha256(code.encode()).hexdigest()
            if record.get('status')=='passed':
                if same: matched+=1
                else: warnings.append(f'Stale test record (not counted): {lang}/{slug}')
    link_count=0
    for page in ROOT.rglob('*.md'):
        if '.git' in page.parts: continue
        text=page.read_text(encoding='utf-8')
        text=re.sub(r'```.*?```','',text,flags=re.S)
        # Strip inline code before link extraction; placeholder paths are not links.
        text=re.sub(r'`[^`]*`','',text)
        links=re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text)
        links+=re.findall(r'(?:src|href)=["\']([^"\']+)["\']',text)
        for link in links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path: continue
            path=(page.parent/unquote(parsed.path)).resolve(); link_count+=1
            check(path.is_relative_to(ROOT) and path.exists(),f'Broken/outside link: {page.relative_to(ROOT)} -> {link}')
    for path in (ROOT/'assets').glob('*.svg'):
        try:
            tree=ET.parse(path)
            check(not any(node.tag.endswith('script') or node.tag.endswith('foreignObject') for node in tree.iter()),f'Unsafe SVG element: {path.name}')
        except ET.ParseError as exc: errors.append(f'Invalid SVG: {path.name}: {exc}')
    for case in read('tests/routing-cases.json'):
        try:
            result=lookup(case['language'],case['query'])
            check(not case.get('error'),f'Route should fail: {case}')
            if 'paths' in case: check(set(result['paths'])==set(case['paths']),f'Route mismatch: {case} -> {result}')
        except ValueError: check(bool(case.get('error')),f'Unexpected route failure: {case}')
    print(f'Coverage: {len(languages)*len(patterns)} detail/source pairs; {link_count} relative links; {matched}/276 hash-matched passes; SKILL.md {len(skill.encode())} bytes / {len(skill.splitlines())} lines')
    for msg in warnings: print('WARNING:',msg)
    for msg in errors: print('ERROR:',msg,file=sys.stderr)
    print('PASS' if not errors else f'FAIL: {len(errors)} errors')
    return int(bool(errors))
if __name__=='__main__': raise SystemExit(main())
