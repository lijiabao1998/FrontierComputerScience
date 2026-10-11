import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'FrontierComputerScience'
RID = '20261011T214605121352Z-gpt-CS-001'
BASE = '8e21cd467c8aeae3c56f44c95e7f6df7103ec403'
NEW = REPO / 'problems/CS-001/experiments/independent_20261011'
OUT = REPO / 'problems/CS-001/results/independent_20261011'
NEW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
(NEW / 'inputs').mkdir(exist_ok=True)

def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

manifest = []
prefix = 'problems/CS-001/experiments/lean-baseline-r1/'
for name in ['vendor/VerifiedCompiler.lean', 'vendor/lakefile.toml', 'vendor/lake-manifest.json', 'vendor/lean-toolchain', 'vendor/LICENSE', 'Boundary.lean', 'FalseControl.lean', 'SorryControl.lean', 'source_manifest.json']:
    rel = prefix + name
    p = subprocess.run(['git', 'show', BASE + ':' + rel], cwd=REPO, capture_output=True, check=True)
    dest = NEW / 'inputs' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(p.stdout)
    manifest.append({'source_path': rel, 'input_path': 'inputs/' + name, 'bytes': len(p.stdout), 'sha256': hashlib.sha256(p.stdout).hexdigest(), 'git_blob': subprocess.check_output(['git', 'rev-parse', BASE + ':' + rel], cwd=REPO, text=True).strip()})
save(NEW / 'INPUT_MANIFEST.json', {'base_commit': BASE, 'files': manifest})
protocol = {
    'id': 'CS-001-independent-kernel-v1', 'round_id': RID, 'source_head': BASE,
    'scope': 'Known public const-folding proof reproduction; no new theorem, performance comparison, unseen test, or parent CS-001 completion.',
    'actual_root': 'Term.constFold_equiv',
    'expected_type': 'forall {tau : Ty} (t : Term tau), Term.Equiv t (Term.constFold t)',
    'toolchain': 'leanprover/lean4:v4.18.0', 'lean_commit': '11ccbced796476be020459a83c599b301a765d3e',
    'lean_sha256': '2efef84b2c0f15b2cb9821c312005e26d631f52e49308e3d531846eb29a8bfac',
    'lake_sha256': 'ef7d519ae107ac31a86ca84b4407a34e737621a7d1134cb9c21073b22cb85d08',
    'budget': {'cpu_affinity_count': 1, 'concurrency': 1, 'usd': 0, 'wall_minutes': 30, 'max_trials': 8, 'per_compile_seconds': 120, 'preparation_started_at': '2026-10-11T21:44:59+00:00', 'hard_deadline': '2026-10-11T22:14:59+00:00', 'installation_excluded': True},
    'closure': {'algorithm': 'Independent Lean Expr recursive constant walker; FIFO breadth-first queue over every ConstantInfo.type and value? true, including opaque values; independently recomputed Python BFS fixed point.', 'metric': 'Elaborated type/value Expr.constants graph; includes core/generated declarations, does not equate to filtered project-only benchmark dependencies or full module/kernel-rule closure.', 'missing_declarations': 'PARTIAL', 'max_unique_declarations': 20000, 'max_queue_entries': 200000, 'allow_axioms': ['propext', 'Classical.choice', 'Quot.sound'], 'reject': ['sorryAx', 'any other axiom', 'reachable unsafe/partial declaration', 'native-named constant', 'Lean.ofReduceBool', 'Lean.ofReduceNat', 'Lean.reduceBool', 'Lean.reduceNat'], 'builtin_collectAxioms': 'Cross-check only; does not replace independent walker or decide missing coverage.'},
    'steps': ['lake build VerifiedCompiler (empty package manifest, no cache)', 'direct lean -t0 -j1 --json of unchanged VerifiedCompiler.lean', 'compile independent AuditSupport.lean', 'ascribe exact universal theorem type, audit actual root', 'compile all seven original Boundary.lean examples', 'original FalseControl.lean must fail with actual rfl/type error', 'admitted SorryControl.lean must compile, independent graph must reach sorryAx and reject', 'custom-axiom fixture must compile and independent audit must reject'],
    'total_verdict': 'PASS only if every required compile/type/boundary/control and closed graph audit succeeds. Tool/import/timeout failures are NOT_RUN/PARTIAL, never successful negative controls. No repeat of this round or deletion of failures.',
    'independence': 'No author reproduce.py, Audit.lean or Closure.lean code/parsers/classifiers imported or reused. Original proof and specified positive/negative Lean fixtures are fixed inputs.',
    'exposure': 'Public complete proof seen before round; no claim of novel autonomous proof search.',
    'reproduction': 'Run verify.py --round-id NEW_ADMITTED_ROUND --attempt NEW_EMPTY_DIRECTORY only after a separately authorized fresh admission; default attempt-1 is exclusive and cannot be replayed.'
}
save(NEW / 'FROZEN_PROTOCOL.json', protocol)
digest = hashlib.sha256((NEW / 'FROZEN_PROTOCOL.json').read_bytes()).hexdigest()
rpath = REPO / 'runs' / RID / 'round.json'
r = json.loads(rpath.read_text(encoding='utf-8'))
assert r['state'] == 'DRAFT' and r['base_sha'] == BASE
r['branch'] = 'gpt/CS-001-kernel-independent-20261011'
r['budget'] = protocol['budget']
r['acceptance'] = 'Frozen FROZEN_PROTOCOL.json SHA256 ' + digest + '; actual kernel/type/seven boundary/false-rfl/sorry/custom controls; closed type/value BFS with exact axiom whitelist. All checks join the total verdict.'
r['not_done'] = 'Known proof reproduction only; no new theorem, unseen proof search, generality/performance result, alternate kernel, or CS-001 parent completion. Prior NOT_RUN artifacts unchanged.'
queries = [
 ('general', '"VeriSoftBench" "Term.constFold_equiv" Lean repository verification 2026'),
 ('discipline', '"verified-compiler" "constFold_equiv" repository Lean 4.18.0'),
 ('solution', '"Term.constFold_equiv" solution proof "Lean"'),
 ('criticism', 'VeriSoftBench Lean axiom audit dependency closure sorryAx native_decide criticism limitations')]
now = dt.datetime.now(dt.timezone.utc).isoformat()
r['preflight'] = {'checked_at': now, 'verdict': 'PARTIAL_PROGRESS', 'queries': [{'category': c, 'query': q, 'searched_at': now} for c, q in queries],
 'sources': [
  {'title': 'VeriSoftBench current arXiv v2 abstract and full HTML', 'url': 'https://arxiv.org/html/2602.18307v2', 'kind': 'primary', 'supports': 'Known repository proof obligations, curated context/oracle limitation and repository dependency scope; current version and limitations read.'},
  {'title': 'VeriSoftBench official repository', 'url': 'https://github.com/utopia-group/VeriSoftBench', 'kind': 'primary', 'supports': 'Public task context; benchmark counts are not this all-core declaration graph.'},
  {'title': 'Pinned public verified-compiler proof', 'url': 'https://github.com/marcusrossel/verified-compiler/tree/4c79694f5b96c6789b307e2911088af6b19540ac', 'kind': 'primary', 'supports': 'Complete prior proof and public exposure; local copied proof hash pinned.'},
  {'title': 'Official Lean 4.18.0 release', 'url': 'https://github.com/leanprover/lean4/releases/tag/v4.18.0', 'kind': 'primary', 'supports': 'Official installation/version commit; local 4.18.0 source read for ConstantInfo and axiom APIs.'}],
 'sources_read': True, 'scope_compared': True, 'retractions_checked': True, 'licenses_checked': True, 'safety_checked': True, 'baseline_identified': True, 'acceptance_frozen': True,
 'limitations': 'Bounded public searches do not prove absence of solutions/retractions. Current arXiv v2 exists, no retraction notice on read pages; known public proof already exists. Source code MIT license copied; source has no external Lake packages. Official compiler trust is explicit, no independent alternate kernel. Expr graph does not expand module bodies or all inductive reduction rules.',
 'scope_comparison': 'Prior fully available Term.constFold_equiv is known progress. Parent problem remains OPEN. This round closes the prior local toolchain NOT_RUN gap for one seen proof and checks independent evaluator behavior.',
 'baseline': 'PR4 exact head, original source/results NOT_RUN retained; upstream source fixed at 4c79694f5b96c6789b307e2911088af6b19540ac. No author classifier used.'}
r['artifacts'] = ['problems/CS-001/experiments/independent_20261011', 'problems/CS-001/results/independent_20261011']
save(rpath, r)
(NEW / '.gitattributes').write_text('* -text\n', encoding='utf-8')
print(json.dumps({'round_id': RID, 'protocol_sha256': digest, 'files': len(manifest), 'state': 'DRAFT', 'no_research_executed': True}))
