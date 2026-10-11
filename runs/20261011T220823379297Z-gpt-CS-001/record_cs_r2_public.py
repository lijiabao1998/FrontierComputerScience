import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
RUN=REPO/'runs/20261011T220823379297Z-gpt-CS-001'
proof=RUN/'evidence/CS_CLAIM_READBACK.json'
j=json.loads(proof.read_text(encoding='utf-8'))
body=(RUN/'evidence/PUBLIC_CLAIM_BODY.md').read_text(encoding='utf-8').strip()
assert j['id']==int(sys.argv[1]) and j['body']==body
rpath=RUN/'round.json'
r=json.loads(rpath.read_text(encoding='utf-8'))
assert r['state']=='DRAFT' and r['independent_static_review']['status']=='PASS'
r['public_claim']={'status':'POSTED_AND_READ_BACK','url':j['html_url'],'comment_id':j['id'],'posted_at':j['created_at'],'readback_at':dt.datetime.now(dt.timezone.utc).isoformat(),'readback_path':str(proof.relative_to(REPO)).replace('\\','/'),'readback_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'body_sha256':hashlib.sha256(body.encode('utf-8')).hexdigest()}
rpath.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for name in ['bind_cs_r2.py','record_cs_r2_public.py']:
    shutil.copyfile(ROOT/name,RUN/name)
print(json.dumps(r['public_claim']))
