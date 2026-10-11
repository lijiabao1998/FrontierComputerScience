import hashlib
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
RUN=REPO/'runs/20261011T214605121352Z-gpt-CS-001'
HERE=REPO/'problems/CS-001/experiments/independent_20261011'
review=ROOT/'evidence/CS_STATIC_REVIEW.json'
rv=json.loads(review.read_text(encoding='utf-8'))
assert rv['verdict']=='PASS'
assert rv['protocol_sha256']==hashlib.sha256((HERE/'FROZEN_PROTOCOL.json').read_bytes()).hexdigest()
assert rv['code_manifest_sha256']==hashlib.sha256((HERE/'CODE_MANIFEST.json').read_bytes()).hexdigest()
for name in ['CS_STATIC_REVIEW.json','CS_STATIC_REVIEW-blocked-v1.json','PUBLIC_CLAIM_BODY.md','current-governance-main.json','current-governance-diff.json']:
    shutil.copyfile(ROOT/'evidence'/name, RUN/'evidence'/name)
rpath=RUN/'round.json'
r=json.loads(rpath.read_text(encoding='utf-8'))
assert r['state']=='DRAFT'
r['independent_static_review']={'status':'PASS','path':str((RUN/'evidence/CS_STATIC_REVIEW.json').relative_to(REPO)).replace('\\','/'),'sha256':hashlib.sha256(review.read_bytes()).hexdigest(),'code_manifest_sha256':rv['code_manifest_sha256']}
r['latest_governance_readback']={'main':'d05c19798f83dd0c19a281e2aa919c1f253cf4e7','pinned':'9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f','diff_files':['PROTOCOL_VERSIONS.md','STATUS.md'],'semantic_gate_change':False,'policy':'Use declared immutable pin; latest documentation confirms CS protocol2.0 pin.'}
rpath.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'static_verdict':'PASS','static_sha256':r['independent_static_review']['sha256'],'official_admission':'PENDING','research':'NOT_RUN'}))
