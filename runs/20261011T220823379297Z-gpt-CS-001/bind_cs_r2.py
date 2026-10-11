import hashlib
import json
import shutil
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
RID='20261011T220823379297Z-gpt-CS-001'
RUN=REPO/'runs'/RID
HERE=REPO/'problems/CS-001/experiments/independent_20261011_r2'
rv_path=ROOT/'evidence/CS_STATIC_REVIEW-r2.json'
rv=json.loads(rv_path.read_text(encoding='utf-8'))
assert rv['verdict']=='PASS'
assert rv['protocol_sha256']==hashlib.sha256((HERE/'FROZEN_PROTOCOL.json').read_bytes()).hexdigest()
assert rv['code_manifest_sha256']==hashlib.sha256((HERE/'CODE_MANIFEST.json').read_bytes()).hexdigest()
shutil.copyfile(rv_path,RUN/'evidence'/rv_path.name)
shutil.copyfile(ROOT/'evidence/CS_ARTIFACT_REVIEW-r1.json',REPO/'runs/20261011T214605121352Z-gpt-CS-001/evidence/CS_ARTIFACT_REVIEW-r1.json')
rpath=RUN/'round.json'
r=json.loads(rpath.read_text(encoding='utf-8'))
assert r['state']=='DRAFT'
r['independent_static_review']={'status':'PASS','path':str((RUN/'evidence'/rv_path.name).relative_to(REPO)).replace('\\','/'),'sha256':hashlib.sha256(rv_path.read_bytes()).hexdigest(),'code_manifest_sha256':rv['code_manifest_sha256']}
rpath.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
body='\n\n'.join([
 'CS-001 repair round '+RID+' - public scope/budget registration before official admit and any r2 research.',
 'Previous round20261011T214605121352Z-gpt-CS-001 is retained as PARTIAL/exit1: source Lake build, direct trust=0 kernel source, seven boundaries and genuine false-rfl rejection passed; independent exporter failed on reserved local identifier at; type/closure/sorry/custom audits remained NOT_RUN. Failed original round cannot replay. Complete raw failures are committed locally at b6e5f8b; no deletion or reclassification.',
 'This separately frozen repair changes only at to cursor in the Lean exporter, new result/round scope, and completed-r1/cumulative guards in the independent Python runner. New protocol SHA256 '+rv['protocol_sha256']+'; code/input manifest SHA256 '+rv['code_manifest_sha256']+'. Independent static review PASS. Fresh four-route searches and current primary pages saved.',
 'Source proof remains pinned PR4 head8e21cd467c8aeae3c56f44c95e7f6df7103ec403; same known public universal theorem Term.constFold_equiv, actual type ascription, elaborated type/value FIFO BFS including opaque values, separate Python fixed-point check, exact axiom whitelist propext/Classical.choice/Quot.sound. Missing declarations PARTIAL; missing modules/tool errors/timeout never negative-control success. Real rfl, admitted sorryAx and custom-axiom controls join total verdict; no author classifier.',
 'Both rounds share one whole-CS budget: preparation start21:44:59 UTC, hard scientific deadline22:14:59 UTC, one CPU, sequential children, USD0. First8 plus repair8 compiler children maximum (cumulative16); each <=120s with bounded owned-process cleanup. No new 30min allocation, extension, or replay of either round. Metadata review/commit/publication may follow after science stops.',
 'Known-proof reproduction only: no novel theorem, unseen search, performance finding, filtered-benchmark dependency comparison or completion of parent CS-001. Official side-by-side installation excluded from research results. Keep all evidence; independent artifact review then local commits/separate stacked draft, no merge/deploy.'
])
(RUN/'evidence/PUBLIC_CLAIM_BODY.md').write_text(body+'\n',encoding='utf-8')
print(json.dumps({'status':'STATIC_PASS','body':body,'round_id':RID},ensure_ascii=True))
