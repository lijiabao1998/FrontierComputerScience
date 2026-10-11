import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
RUN=REPO/'runs/20261011T214605121352Z-gpt-CS-001'
rpath=RUN/'round.json'
r=json.loads(rpath.read_text(encoding='utf-8'))
result=json.loads((REPO/'problems/CS-001/results/independent_20261011/attempt-1/RESULT.json').read_text(encoding='utf-8'))
assert result['verdict']=='PARTIAL_OR_FAILED_INDEPENDENT_KERNEL_VALIDATION'
r['state']='FINISHED'
r['result']={'status':'PARTIAL_CLOSURE_NOT_RUN','checks':result['checks'],'started_at':result['started_at'],'finished_at':result['finished_at'],'failure':'AuditSupport.lean line37 uses Lean reserved keyword at; exporter fails, downstream AuditSupport imports fail. No actual closure/type/sorry/custom result.','parent_problem':'OPEN','usd':0,'no_replay':True}
rpath.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for p in (ROOT/'evidence/commands').iterdir():
    if p.is_file():
        shutil.copyfile(p,RUN/'evidence/commands'/p.name)
for name in ['bind_cs_admission.py','record_cs_public.py','preserve_cs_r1.py']:
    shutil.copyfile(ROOT/name,RUN/name)
print(json.dumps({'original_round':'FINISHED_PARTIAL','replayed':False,'all_failures_retained':True}))
