#!/usr/bin/env python3
"""Gán mô tả + nguồn đã tra cho từng mốc. Dùng: python3 _build/setrec.py < data.json"""
import json,sys,pathlib
EV=pathlib.Path(__file__).resolve().parent/'events.json'
ev=json.loads(EV.read_text(encoding='utf-8')); b={e['id']:e for e in ev}
recs=json.load(sys.stdin)
for r in recs:
    e=b[r['id']]
    e['description']=r['description']; e['source']=r['source']; e['sourceUrl']=r.get('url','')
EV.write_text(json.dumps(ev,ensure_ascii=False,indent=1),encoding='utf-8')
done=[e['id'] for e in ev if e['source']!='[Chưa có nguồn trích dẫn trong tài liệu gốc]']
print(f"đã gán {len(recs)} mốc | tổng đã có nguồn: {len(done)}/81")
print('còn lại:',[e['id'] for e in ev if e['source']=='[Chưa có nguồn trích dẫn trong tài liệu gốc]'][:14],'...')
