import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT/'FrontierComputerScience'
RUN=REPO/'runs/20261011T220823379297Z-gpt-CS-001'
for p in (ROOT/'evidence/commands').iterdir():
    if p.is_file() and not p.name.startswith('cs-capture-final'):
        shutil.copyfile(p,RUN/'evidence/commands'/p.name)
shutil.copyfile(ROOT/'capture_cs_final_evidence.py',RUN/'capture_cs_final_evidence.py')
print(json.dumps({'metadata_only':True,'scientific_processes_launched':0,'existing_command_evidence_archived':True}))
