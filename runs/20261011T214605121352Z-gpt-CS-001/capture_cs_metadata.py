import datetime as dt
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'FrontierComputerScience'
RUN = REPO / 'runs/20261011T214605121352Z-gpt-CS-001'
BASE = '8e21cd467c8aeae3c56f44c95e7f6df7103ec403'
tree = subprocess.check_output(['git', 'ls-tree', '-rz', BASE], cwd=REPO)
(RUN / 'original-tree.raw.txt').write_bytes(tree)
rows = []
for raw in tree.split(b'\0'):
    if raw:
        meta, path = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode('ascii').split()
        rows.append({'path': path.decode('utf-8'), 'mode': mode, 'type': kind, 'oid': oid})
(RUN / 'ORIGINAL_TREE.json').write_text(json.dumps({'base': BASE, 'entries': rows}, indent=2) + '\n', encoding='utf-8')
for path in (ROOT / 'evidence').glob('current-*.json'):
    shutil.copyfile(path, RUN / 'evidence' / path.name)
notes = {'captured_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'scientific_run_started': False, 'preparation_commands': [
 {'script': 'prepare_cs.py', 'exit_code': 0, 'stdout_metadata': {'protocol_sha256': '476237eba91b0369b057941f1bbf5d248134b11d7fd9d214b286e6a82b3eca97', 'files': 9}},
 {'script': 'seal_cs.py', 'exit_code': 0, 'stdout_metadata': {'manifest_sha256': 'dcb9ec1da57a689c1dc600518e987ea7c9797552199d1faf0397ce19d1be2dec', 'files': 16}},
 {'script': 'refreeze_cs.py', 'exit_code': 0, 'protocol_sha256': '6da66f63a40751154b5cbd0beee60a6787a7825e9a7956cdff4533622c850a6a', 'first_revision_manifest': 'd0100b0aeac16d23121f1780f01f459551e8adafc69dfa6716900dcd74b74b5d', 'final_manifest': '17dfe4689c9fc5d485c7d497b6edd485312ff9dfcb76d03ad15974c708ea328c'}],
 'python_runtime_warning_preserved': 'Failed to find real location of C:\\Users\\Leon1\\AppData\\Local\\Programs\\Python\\Python313\\python.exe',
 'read_failures': ['An early read incorrectly targeted problems/CS-001.md; actual card is problems/CS-001/problem.json, subsequently read.', 'An early reuse lookup targeted guard.py; actual previous file is admission_guard.py, subsequently read.', 'Repository .agents directory returned 404; local inventory also found none.'],
 'failure_evidence_limit': 'Early read-command outputs and preparation invocations were returned by tool UI before the dedicated exec_logged wrapper; this metadata records them rather than inventing separately captured raw stdout/stderr. Scientific invocation and every compiler child use dedicated raw files.',
 'research_installation_separation': 'Official Elan install completed 21:43:57.294226 UTC before conservative round start 21:44:59 UTC; not a research result or budget charge.',
 'independent_preflight_rejection': 'BLOCKED static review retained as CS_STATIC_REVIEW-blocked-v1.json; repairs occurred before admission/any research.', 'source_original_file_count': len(rows)}
(RUN / 'PREPARATION_NOTES.json').write_text(json.dumps(notes, indent=2) + '\n', encoding='utf-8')
for name in ['refreeze_cs.py', 'capture_cs_metadata.py']:
    shutil.copyfile(ROOT / name, RUN / name)
print(json.dumps({'original_entries': len(rows), 'no_research_executed': True}))
