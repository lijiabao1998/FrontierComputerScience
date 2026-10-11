import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'FrontierComputerScience'
HERE = REPO / 'problems/CS-001/experiments/independent_20261011'
def save(p, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
p = json.loads((HERE / 'FROZEN_PROTOCOL.json').read_text(encoding='utf-8'))
p['exclusive_launch'] = 'Frozen protocol/round/budget identity; exact attempt-1 only; round RESEARCH_LAUNCH_EXCLUSIVE.json opened with x mode prevents replay under another attempt name.'
p['bounded_cleanup'] = 'Each compile wait <=116 seconds minus spawn overhead and entire deadline remaining minus4; taskkill owned process tree timeout2, wait1, fallback kill/wait1; no next child if prior child remains. Reserve5 seconds before spawning.'
save(HERE / 'FROZEN_PROTOCOL.json', p)
digest = hashlib.sha256((HERE / 'FROZEN_PROTOCOL.json').read_bytes()).hexdigest()
rpath = REPO / 'runs' / p['round_id'] / 'round.json'
r = json.loads(rpath.read_text(encoding='utf-8'))
assert r['state'] == 'DRAFT'
r['acceptance'] = 'Frozen FROZEN_PROTOCOL.json SHA256 ' + digest + '; actual kernel/type/seven boundary/false-rfl/sorry/custom controls; closed type/value BFS with exact axiom whitelist. All checks join total verdict; bounded cleanup and exclusive round launch.'
save(rpath, r)
paths = [x for x in HERE.rglob('*') if x.is_file() and x.name != 'CODE_MANIFEST.json']
save(HERE / 'CODE_MANIFEST.json', {'files': [{'path': str(x.relative_to(HERE)).replace('\\', '/'), 'bytes': x.stat().st_size, 'sha256': hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(paths)]})
print(json.dumps({'protocol_sha256': digest, 'manifest_sha256': hashlib.sha256((HERE / 'CODE_MANIFEST.json').read_bytes()).hexdigest(), 'files': len(paths), 'no_research_executed': True}))
