#!/usr/bin/env python3
"""Resolve known language/pattern aliases to real local pages (not semantic search)."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def normalize(value: str) -> str:
    return re.sub(r'[\s_-]+','',value.casefold()).removesuffix('模式')

def lookup(language: str, query: str = '', root: Path = ROOT) -> dict:
    catalog=json.loads((root/'catalog.json').read_text(encoding='utf-8'))
    languages=catalog['languages']; target=normalize(language)
    candidates=[slug for slug,item in languages.items() if target in {normalize(slug),normalize(item['name']),*(normalize(a) for a in item['aliases'])}]
    if len(candidates)!=1: raise ValueError('Unsupported or ambiguous language: '+language)
    slug=candidates[0]; lang=languages[slug]
    if not query.strip(): return {'language':slug,'type':'index','paths':[lang['index']]}
    target=normalize(query)
    matched=[p for p,item in catalog['patterns'].items() if target in {normalize(p),normalize(item['name']),normalize(item['english']),*(normalize(a) for a in item['aliases'])}]
    # For a sentence, match complete English names or explicit Chinese aliases only.
    if not matched:
        q=query.casefold()
        for p,item in catalog['patterns'].items():
            for alias in item['aliases']:
                if any('\u4e00' <= c <= '\u9fff' for c in alias): found=alias in q
                else: found=bool(re.search(r'(?<![\w-])'+re.escape(alias.casefold())+r'(?![\w-])',q))
                if found: matched.append(p); break
    paths=[lang['patterns'][p] for p in dict.fromkeys(matched)] if matched else [lang['index']]
    if not all((root/path).is_file() for path in paths): raise FileNotFoundError('Catalog route is missing; run scripts/build.py')
    result={'language':slug,'type':'patterns' if matched else 'index','paths':paths}
    if not matched: result['note']='No exact pattern alias matched; consult this language index. No pattern was inferred.'
    return result

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--language',required=True); parser.add_argument('--query',default='')
    args=parser.parse_args()
    try: print(json.dumps(lookup(args.language,args.query),ensure_ascii=False,indent=2)); return 0
    except (ValueError,FileNotFoundError) as exc: print(str(exc),file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
