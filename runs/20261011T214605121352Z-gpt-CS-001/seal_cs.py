import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'FrontierComputerScience'
RID = '20261011T214605121352Z-gpt-CS-001'
NEW = REPO / 'problems/CS-001/experiments/independent_20261011'
RUN = REPO / 'runs' / RID
def save(p, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
paths = [p for p in NEW.rglob('*') if p.is_file() and p.name not in ['CODE_MANIFEST.json']]
save(NEW / 'CODE_MANIFEST.json', {'files': [{'path': str(p.relative_to(NEW)).replace('\\', '/'), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]})
rpath = RUN / 'round.json'
r = json.loads(rpath.read_text(encoding='utf-8'))
assert r['state'] == 'DRAFT'
for q in r['preflight']['queries']:
    q.pop('searched_at', None)
    q['engine'] = 'OpenAI web search'
    q['outcome'] = 'Known public proof/benchmark found; bounded search does not certify absence of solutions or retractions. See saved raw search and primary-page evidence.'
save(rpath, r)
for source in ['installation', 'evidence']:
    dest = RUN / source
    if dest.exists():
        raise RuntimeError('Sealing is exclusive; do not overwrite evidence')
    shutil.copytree(ROOT / source, dest)
for name in ['install_lean.py', 'get_cs_source.py', 'prepare_cs.py', 'seal_cs.py', 'RESEARCH_PREPARATION_START.json']:
    shutil.copyfile(ROOT / name, RUN / name)
(REPO / 'problems/CS-001/results/independent_20261011/.gitignore').write_text('*.olean\n*.ilean\n*.c\n*.o\n*.a\n*.dll\n.lake/\n__pycache__/\n', encoding='utf-8')
print(json.dumps({'manifest_sha256': hashlib.sha256((NEW / 'CODE_MANIFEST.json').read_bytes()).hexdigest(), 'files': len(paths), 'no_research_executed': True}))
