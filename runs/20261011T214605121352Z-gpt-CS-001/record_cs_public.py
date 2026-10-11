import datetime as dt
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
RUN=REPO/'runs/20261011T214605121352Z-gpt-CS-001'
proof=RUN/'evidence/CS_CLAIM_CORRECTED_READBACK.json'
j=json.loads(proof.read_text(encoding='utf-8'))
body=(ROOT/'evidence/PUBLIC_CLAIM_BODY.md').read_text(encoding='utf-8').strip()
assert j['id']==6114320766 and j['body']==body
rpath=RUN/'round.json'
r=json.loads(rpath.read_text(encoding='utf-8'))
assert r['state']=='ADMITTED' and r['independent_static_review']['status']=='PASS'
r['public_claim']={'status':'POSTED_AND_READ_BACK','url':j['html_url'],'comment_id':j['id'],'posted_at':j['created_at'],'readback_at':dt.datetime.now(dt.timezone.utc).isoformat(),'readback_path':str(proof.relative_to(REPO)).replace('\\','/'),'readback_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'body_sha256':hashlib.sha256(body.encode('utf-8')).hexdigest()}
r['public_claim']['initial_readback_path']=str((RUN/'evidence/CS_CLAIM_READBACK.json').relative_to(REPO)).replace('\\','/')
r['public_claim']['sequence_note']='Initial public scope, budget and all protocol/source hashes were posted/read back before admit. Complete-string binding failed only for a PowerShell-decoded em dash; official admit proceeded before local binding. Same comment cosmetic text corrected and exact readback bound before protocol commit and any research. No scope/budget/hash change; raw initial readback and failed binding logs retained.'
rpath.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(RUN/'.gitattributes').write_text('* -text\n',encoding='utf-8')
(REPO/'problems/CS-001/results/independent_20261011/.gitattributes').write_text('* -text\n',encoding='utf-8')
print(json.dumps(r['public_claim']))
