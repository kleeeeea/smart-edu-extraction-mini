"""Read reviewed CSV records without mutating the source."""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]

def read_csv(path):
    rows=list(csv.reader(io.StringIO(path.read_text(encoding='utf-8-sig'),newline=''),strict=True))
    index=next(i for i,r in enumerate(rows) if r and r[0]=='knowledge_point_id')
    return [dict(zip(rows[index],r)) for r in rows[index+1:] if any(r)]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--book')
    p.add_argument('--id')
    p.add_argument('--keyword')
    a=p.parse_args()
    books=json.loads((ROOT/'references/books.json').read_text(encoding='utf-8'))
    out=[]
    for b in books:
        if a.book and a.book not in (b['book'],b['slug']):
            continue
        for r in read_csv(ROOT/b['source_csv']):
            if a.id and r['knowledge_point_id']!=a.id:
                continue
            if a.keyword and a.keyword not in ' '.join(r.values()):
                continue
            out.append({'book':b['book'],**r})
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
