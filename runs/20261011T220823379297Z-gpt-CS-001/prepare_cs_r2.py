import datetime as dt
import hashlib
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
OLD_ID='20261011T214605121352Z-gpt-CS-001'
RID='20261011T220823379297Z-gpt-CS-001'
OLD=REPO/'problems/CS-001/experiments/independent_20261011'
HERE=REPO/'problems/CS-001/experiments/independent_20261011_r2'
RUN=REPO/'runs'/RID
OUT=REPO/'problems/CS-001/results/independent_20261011_r2'
shutil.copytree(OLD,HERE)
support=HERE/'AuditSupport.lean'
s=support.read_text(encoding='utf-8')
s=s.replace('let mut at := 0','let mut cursor := 0').replace('while at <','while cursor <').replace('queue[at]!','queue[cursor]!').replace('at := at + 1','cursor := cursor + 1').replace('toJson at)','toJson cursor)')
support.write_text(s,encoding='utf-8')
vp=HERE/'verify.py'
v=vp.read_text(encoding='utf-8').replace('independent_20261011','independent_20261011_r2')
v=v.replace("assert b == protocol['budget'], 'NOT_RUN: exact frozen budget mismatch'", "assert b == protocol['budget'], 'NOT_RUN: exact frozen budget mismatch'\n    previous = json.loads((REPO / 'problems/CS-001/results/independent_20261011/attempt-1/RESULT.json').read_text(encoding='utf-8'))\n    assert previous['verdict'] == 'PARTIAL_OR_FAILED_INDEPENDENT_KERNEL_VALIDATION' and len(previous['steps']) == 8, 'NOT_RUN: prior round did not finish as the preserved eight-step partial'\n    assert protocol['cumulative_compile_cap'] == 16, 'NOT_RUN: cumulative CS compile cap changed'")
vp.write_text(v,encoding='utf-8')
def save(p,obj):
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=json.loads((HERE/'FROZEN_PROTOCOL.json').read_text(encoding='utf-8'))
p['id']='CS-001-independent-kernel-repair-v2'
p['round_id']=RID
p['repair_of_round']=OLD_ID
p['prior_round_verdict']='PARTIAL_OR_FAILED_INDEPENDENT_KERNEL_VALIDATION'
p['repair_delta']='Rename Lean reserved local identifier at to cursor; frozen r1 source/manifest/results never edited. Separate runner result scope and explicit completed-r1/cumulative guards.'
p['cumulative_compile_cap']=16
p['shared_CS_budget']='Both rounds share the original preparation start21:44:59 and harddeadline22:14:59; no new allocation, extension or rerun of r1.'
save(HERE/'FROZEN_PROTOCOL.json',p)
proto_sha=hashlib.sha256((HERE/'FROZEN_PROTOCOL.json').read_bytes()).hexdigest()
paths=[x for x in HERE.rglob('*') if x.is_file() and x.name!='CODE_MANIFEST.json']
save(HERE/'CODE_MANIFEST.json',{'files':[{'path':str(x.relative_to(HERE)).replace('\\','/'),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(paths)]})
manifest_sha=hashlib.sha256((HERE/'CODE_MANIFEST.json').read_bytes()).hexdigest()
old_r=json.loads((REPO/'runs'/OLD_ID/'round.json').read_text(encoding='utf-8'))
rpath=RUN/'round.json'
r=json.loads(rpath.read_text(encoding='utf-8'))
assert r['state']=='DRAFT'
r['branch']='gpt/CS-001-kernel-independent-20261011'
r['budget']=p['budget']
r['acceptance']='Frozen repair protocol SHA256 '+proto_sha+'; same exact universal theorem/type-value BFS/axiom whitelist/all8 checks and cumulative16 children/shared original deadline.'
r['not_done']=old_r['not_done']
r['preflight']=old_r['preflight']
r['preflight']['checked_at']=dt.datetime.now(dt.timezone.utc).isoformat()
queries=['"VeriSoftBench" "Term.constFold_equiv" Lean verification','"verified-compiler" "constFold_equiv" "4.18.0"','"Term.constFold_equiv" solution proof Lean','VeriSoftBench dependency closure axiom sorryAx limitations criticism']
for q,text in zip(r['preflight']['queries'],queries):
    q['query']=text
    q['outcome']='Fresh repair-round query after new official start; known proof and benchmark already public. See CS_R2_FRESH_SEARCH.json. No new theorem/absence claim.'
r['preflight']['baseline']='Finished r1 PARTIAL (reserved at in independent exporter), exact raw failures retained in local commit. Same unchanged upstream proof, no author classifier.'
r['preflight']['scope_comparison']='Minimal executable harness repair in a separate admitted round within the same whole-CS 30min budget; r1 cannot replay, cumulative child cap16, parent remains OPEN.'
r['artifacts']=['problems/CS-001/experiments/independent_20261011_r2','problems/CS-001/results/independent_20261011_r2']
save(rpath,r)
OUT.mkdir()
(OUT/'.gitattributes').write_text('* -text\n',encoding='utf-8')
shutil.copyfile(REPO/'problems/CS-001/results/independent_20261011/.gitignore',OUT/'.gitignore')
(RUN/'.gitattributes').write_text('* -text\n',encoding='utf-8')
(RUN/'evidence').mkdir()
shutil.copyfile(ROOT/'evidence/CS_R2_FRESH_SEARCH.json',RUN/'evidence/CS_R2_FRESH_SEARCH.json')
shutil.copyfile(ROOT/'prepare_cs_r2.py',RUN/'prepare_cs_r2.py')
print(json.dumps({'round_id':RID,'protocol_sha256':proto_sha,'manifest_sha256':manifest_sha,'no_r2_research':True,'hard_deadline':'22:14:59 UTC'}))
