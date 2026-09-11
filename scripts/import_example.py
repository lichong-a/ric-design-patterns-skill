#!/usr/bin/env python3
"""Update one canonical example from a reviewed UTF-8 source file; never execute it."""
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--language',required=True); p.add_argument('--pattern',required=True)
    p.add_argument('--file',required=True,type=Path); p.add_argument('--idiom',help='Optional replacement implementation note')
    args=p.parse_args()
    languages={l['slug'] for l in json.loads((ROOT/'data/languages.json').read_text())}
    if args.language not in languages: p.error('Unknown language slug')
    path=ROOT/'data/code'/f'{args.language}.json'; bank=json.loads(path.read_text(encoding='utf-8'))
    if args.pattern not in bank: p.error('Unknown pattern slug')
    try: code=args.file.read_text(encoding='utf-8')
    except (OSError,UnicodeError) as exc: p.error(str(exc))
    if not code.strip(): p.error('Source must not be empty')
    bank[args.pattern]['code']=code.rstrip()+'\n'
    if args.idiom is not None: bank[args.pattern]['idiom']=args.idiom
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Canonical source updated; rebuild, rerun this language and rebuild again. Old hash evidence will not validate changed source.')
if __name__=='__main__': main()
