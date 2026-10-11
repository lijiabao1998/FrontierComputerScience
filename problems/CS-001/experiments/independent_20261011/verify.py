"""One admitted, exclusive, sequential kernel run. No author classifier is used."""
import argparse
import collections
import ctypes
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
UTC = dt.timezone.utc
TOOLCHAIN = Path(r'C:\Users\Leon1\.elan\toolchains\leanprover--lean4---v4.18.0')

def now():
    return dt.datetime.now(UTC).isoformat()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def graph_audit(path, expected_root):
    if not path.exists():
        return {'status': 'PARTIAL', 'reason': 'No elaborated closure artifact'}
    try:
        g = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, OSError) as exc:
        return {'status': 'PARTIAL', 'reason': 'Unreadable graph', 'exception': repr(exc)}
    if not isinstance(g, dict) or g.get('schema') != 'independent-type-value-bfs-v1' or g.get('root') != expected_root or g.get('opaque_values_included') is not True:
        return {'status': 'PARTIAL', 'reason': 'Wrong graph schema/root/opaque coverage'}
    nodes = g.get('nodes', [])
    kinds = ['axiom', 'definition', 'theorem', 'opaque', 'quotient', 'inductive', 'constructor', 'recursor']
    if not isinstance(nodes, list) or len(nodes) > 20000 or not isinstance(g.get('missing'), list) or type(g.get('processed_queue_entries')) is not int or not 0 <= g['processed_queue_entries'] <= 200000:
        return {'status': 'PARTIAL', 'reason': 'Malformed graph or exceeded closure cap'}
    if not isinstance(g.get('builtin_axioms'), list) or not all(isinstance(a, str) for a in g['builtin_axioms']) or len(g['builtin_axioms']) != len(set(g['builtin_axioms'])):
        return {'status': 'PARTIAL', 'reason': 'Malformed official cross-check'}
    for n in nodes:
        if not isinstance(n, dict) or not isinstance(n.get('name'), str) or not n['name'] or n.get('kind') not in kinds or any(type(n.get(k)) is not bool for k in ['unsafe', 'partial', 'has_value']) or any(not isinstance(n.get(k), list) or not all(isinstance(a, str) and a for a in n[k]) for k in ['type_refs', 'value_refs']):
            return {'status': 'PARTIAL', 'reason': 'Malformed declaration node'}
    by_name = {n['name']: n for n in nodes}
    if len(by_name) != len(nodes) or g.get('missing') or g.get('complete') is not True:
        return {'status': 'PARTIAL', 'reason': 'Duplicate or missing declarations', 'missing': g.get('missing')}
    queue = collections.deque([expected_root])
    distance = {expected_root: 0}
    edge_count = 0
    while queue:
        name = queue.popleft()
        if name not in by_name:
            return {'status': 'PARTIAL', 'reason': 'Referenced declaration missing', 'name': name}
        n = by_name[name]
        for field in ['type_refs', 'value_refs']:
            refs = n[field]
            if len(refs) != len(set(refs)) or not all(isinstance(x, str) for x in refs):
                return {'status': 'PARTIAL', 'reason': 'Malformed expression references'}
            edge_count += len(refs)
            for ref in refs:
                if ref not in distance:
                    distance[ref] = distance[name] + 1
                    queue.append(ref)
    if set(distance) != set(by_name):
        return {'status': 'PARTIAL', 'reason': 'Export is not precisely the reached fixed point'}
    axioms = sorted(n['name'] for n in nodes if n['kind'] == 'axiom')
    if set(axioms) != set(g.get('builtin_axioms', [])):
        return {'status': 'PARTIAL', 'reason': 'Independent graph axiom set differs from official cross-check', 'axioms': axioms, 'builtin_axioms': g.get('builtin_axioms')}
    forbidden_axioms = [a for a in axioms if a not in ['propext', 'Classical.choice', 'Quot.sound']]
    dangerous = sorted(n['name'] for n in nodes if n.get('unsafe') is not False or n.get('partial') is not False or 'native' in n['name'].lower() or n['name'] in ['Lean.ofReduceBool', 'Lean.ofReduceNat', 'Lean.reduceBool', 'Lean.reduceNat'] or 'sorryAx' in n['name'].split('.'))
    root_kind = by_name[expected_root]['kind']
    result = {'status': 'REJECT' if forbidden_axioms or dangerous or root_kind != 'theorem' else 'PASS', 'root': expected_root, 'root_kind': root_kind, 'unique_declarations': len(nodes), 'type_value_edges': edge_count, 'maximum_bfs_distance': max(distance.values()), 'axioms': axioms, 'forbidden_axioms': forbidden_axioms, 'dangerous_declarations': dangerous, 'kind_counts': dict(sorted(collections.Counter(n['kind'] for n in nodes).items())), 'graph_sha256': sha(path), 'missing_count': 0, 'fixed_point_complete': True}
    save(path.with_name(path.stem + '-independent-audit.json'), result)
    return result

def messages(raw):
    parsed = []
    for line in raw.decode('utf-8', errors='replace').splitlines():
        if line.strip():
            try:
                parsed.append(json.loads(line))
            except json.JSONDecodeError:
                parsed.append({'unparsed': line})
    return parsed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--round-id', required=True)
    ap.add_argument('--attempt', required=True)
    args = ap.parse_args()
    protocol_path = HERE / 'FROZEN_PROTOCOL.json'
    protocol = json.loads(protocol_path.read_text(encoding='utf-8'))
    r = json.loads((REPO / 'runs' / args.round_id / 'round.json').read_text(encoding='utf-8'))
    assert protocol['round_id'] == args.round_id == r['round_id'], 'NOT_RUN: different round identity'
    assert r.get('problem_id') == 'CS-001' and r.get('state') in ('ADMITTED', 'RUNNING') and r.get('admitted_at'), 'NOT_RUN: admission absent'
    assert r['preflight']['verdict'] == 'PARTIAL_PROGRESS' and sha(protocol_path) in r['acceptance'], 'NOT_RUN: frozen protocol/admission mismatch'
    claim = r.get('public_claim', {})
    assert claim.get('status') == 'POSTED_AND_READ_BACK' and sha(REPO / claim['readback_path']) == claim['readback_sha256'], 'NOT_RUN: public readback missing'
    static = r.get('independent_static_review', {})
    assert static.get('status') == 'PASS' and sha(REPO / static['path']) == static['sha256'], 'NOT_RUN: independent static approval missing'
    manifest_path = HERE / 'CODE_MANIFEST.json'
    assert sha(manifest_path) == static['code_manifest_sha256'], 'NOT_RUN: review covers a different code manifest'
    for item in json.loads(manifest_path.read_text(encoding='utf-8'))['files']:
        assert sha(HERE / item['path']) == item['sha256'], 'NOT_RUN: frozen executable/input changed'
    b = r['budget']
    assert b == protocol['budget'], 'NOT_RUN: exact frozen budget mismatch'
    assert b['cpu_affinity_count'] == b['concurrency'] == 1 and b['usd'] == 0 and b['max_trials'] == 8, 'NOT_RUN: budget contract changed'
    deadline = dt.datetime.fromisoformat(b['hard_deadline'])
    assert dt.datetime.now(UTC) < deadline, 'NOT_RUN: entire round budget expired'
    out = Path(args.attempt).resolve()
    assert out == (REPO / 'problems/CS-001/results/independent_20261011/attempt-1').resolve(), 'NOT_RUN: this round has exactly one attempt-1'
    marker = REPO / 'runs' / args.round_id / 'RESEARCH_LAUNCH_EXCLUSIVE.json'
    with marker.open('x', encoding='utf-8') as f:
        json.dump({'started_at': now(), 'round_id': args.round_id, 'attempt': str(out)}, f)
    out.mkdir(parents=True, exist_ok=False)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    kernel.GetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1), 'NOT_RUN: cannot bound CPU'
    lean = TOOLCHAIN / 'bin/lean.exe'
    lake = TOOLCHAIN / 'bin/lake.exe'
    assert sha(lean) == protocol['lean_sha256'] and sha(lake) == protocol['lake_sha256'], 'NOT_RUN: tool binaries changed'
    scratch = out / 'scratch'
    shutil.copytree(HERE / 'inputs/vendor', scratch)
    for name in ['AuditSupport.lean', 'TheoremProbe.lean', 'CustomControl.lean']:
        shutil.copyfile(HERE / name, scratch / name)
    for name in ['Boundary.lean', 'FalseControl.lean']:
        shutil.copyfile(HERE / 'inputs' / name, scratch / name)
    sorry = (HERE / 'inputs/SorryControl.lean').read_text(encoding='utf-8')
    (scratch / 'SorryAudit.lean').write_text('import AuditSupport\n' + sorry + '\n#cs_audit forbiddenAdmission "sorry-closure.json"\n', encoding='utf-8')
    env = os.environ.copy()
    env.update({'PATH': str(TOOLCHAIN / 'bin') + os.pathsep + env.get('PATH', ''), 'ELAN_TOOLCHAIN': 'leanprover/lean4:v4.18.0', 'LEAN_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'PYTHONHASHSEED': '0'})
    steps = []
    aborted = False
    started = now()
    save(out / 'LAUNCH.json', {'started_at': started, 'protocol_sha256': sha(protocol_path), 'code_manifest_sha256': sha(manifest_path), 'round_id': args.round_id, 'parent_pid': os.getpid(), 'affinity_mask': 1, 'deadline': deadline.isoformat(), 'usd': 0, 'installation_counted_as_result': False})
    def run(label, cmd):
        nonlocal aborted
        if aborted or len(steps) >= 8 or (deadline - dt.datetime.now(UTC)).total_seconds() <= 5:
            rec = {'label': label, 'command': cmd, 'status': 'NOT_RUN', 'reason': 'budget exhausted'}
            steps.append(rec)
            save(out / (label + '.json'), rec)
            return rec
        rec = {'label': label, 'command': cmd, 'cwd': str(scratch), 'started_at': now(), 'timeout_seconds': min(116, (deadline - dt.datetime.now(UTC)).total_seconds() - 4)}
        tic = time.perf_counter()
        p = None
        cleanup_attempted = False
        def cleanup():
            nonlocal aborted, cleanup_attempted
            if p is None or p.poll() is not None:
                return
            if cleanup_attempted:
                aborted = True
                rec['orphaned_child'] = True
                return
            cleanup_attempted = True
            try:
                kill = subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True, timeout=2)
                (out / (label + '.kill.stdout.txt')).write_bytes(kill.stdout)
                (out / (label + '.kill.stderr.txt')).write_bytes(kill.stderr)
                rec['kill_exit_code'] = kill.returncode
            except subprocess.TimeoutExpired as exc:
                (out / (label + '.kill.stdout.txt')).write_bytes(exc.stdout or b'')
                (out / (label + '.kill.stderr.txt')).write_bytes(exc.stderr or b'')
                rec['kill_timed_out'] = True
            except OSError as exc:
                rec['kill_exception'] = repr(exc)
            try:
                p.wait(timeout=1)
            except subprocess.TimeoutExpired:
                p.kill()
                try:
                    p.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    aborted = True
                    rec['orphaned_child'] = True
            rec['child_terminated'] = p.poll() is not None
            if not rec['child_terminated']:
                aborted = True
        try:
            with (out / (label + '.stdout.txt')).open('xb') as stdout, (out / (label + '.stderr.txt')).open('xb') as stderr:
                if (deadline - dt.datetime.now(UTC)).total_seconds() <= 5:
                    raise RuntimeError('Deadline too near to launch a bounded child')
                p = subprocess.Popen(cmd, cwd=scratch, env=env, stdout=stdout, stderr=stderr)
                rec['pid'] = p.pid
                pm, sm = ctypes.c_size_t(), ctypes.c_size_t()
                ok = kernel.GetProcessAffinityMask(ctypes.c_void_p(int(p._handle)), ctypes.byref(pm), ctypes.byref(sm))
                rec['affinity_mask'] = pm.value if ok else None
                if not ok or pm.value != 1:
                    cleanup()
                    raise RuntimeError('Child affinity not verified as one CPU')
                try:
                    remaining = min(116 - (time.perf_counter() - tic), (deadline - dt.datetime.now(UTC)).total_seconds() - 4)
                    if remaining <= 0:
                        raise subprocess.TimeoutExpired(cmd, 0)
                    rec['exit_code'] = p.wait(timeout=remaining)
                    rec['timed_out'] = False
                except subprocess.TimeoutExpired:
                    cleanup()
                    rec.update({'exit_code': p.returncode, 'timed_out': True})
                rec['status'] = 'EXIT_RECORDED'
        except Exception as exc:
            if p is not None and p.poll() is None:
                cleanup()
            rec.update({'status': 'NOT_RUN', 'exception': repr(exc)})
        rec.update({'finished_at': now(), 'wall_seconds': time.perf_counter() - tic})
        for stream in ['stdout', 'stderr']:
            f = out / (label + '.' + stream + '.txt')
            if f.exists():
                rec[stream + '_bytes'] = f.stat().st_size
                rec[stream + '_sha256'] = sha(f)
        save(out / (label + '.json'), rec)
        steps.append(rec)
        return rec
    def success(rec):
        return rec.get('exit_code') == 0 and rec.get('timed_out') is False and rec.get('affinity_mask') == 1
    lake_rec = run('01-lake-build', [str(lake), '--no-cache', '--no-ansi', '--verbose', 'build', 'VerifiedCompiler'])
    oleans = list((scratch / '.lake/build').rglob('VerifiedCompiler.olean'))
    env['LEAN_PATH'] = os.pathsep.join([str(scratch), str(oleans[0].parent) if len(oleans) == 1 else str(scratch / 'MISSING_IMPORTS'), str(TOOLCHAIN / 'lib/lean')])
    kernel_rec = run('02-kernel-source', [str(lean), '-t0', '-j1', '--json', '-o', 'kernel-VerifiedCompiler.olean', 'VerifiedCompiler.lean'])
    support = run('03-audit-support', [str(lean), '-t0', '-j1', '--json', '-o', 'AuditSupport.olean', 'AuditSupport.lean'])
    theorem = run('04-type-root-closure', [str(lean), '-t0', '-j1', '--json', 'TheoremProbe.lean'])
    boundary = run('05-seven-boundaries', [str(lean), '-t0', '-j1', '--json', 'Boundary.lean'])
    false = run('06-false-conjunction', [str(lean), '-t0', '-j1', '--json', 'FalseControl.lean'])
    sorry_rec = run('07-sorry-control', [str(lean), '-t0', '-j1', '--json', 'SorryAudit.lean'])
    custom_rec = run('08-custom-axiom', [str(lean), '-t0', '-j1', '--json', 'CustomControl.lean'])
    root_audit = graph_audit(scratch / 'theorem-closure.json', 'Term.constFold_equiv')
    sorry_audit = graph_audit(scratch / 'sorry-closure.json', 'forbiddenAdmission')
    custom_audit = graph_audit(scratch / 'custom-closure.json', 'forbiddenCustom')
    fm = messages((out / '06-false-conjunction.stdout.txt').read_bytes()) if (out / '06-false-conjunction.stdout.txt').exists() else []
    errors = [m for m in fm if m.get('severity') == 'error']
    def rfl_error(m):
        data = str(m.get('data', ''))
        return ('rfl' in data and ('failed' in data or 'type mismatch' in data)) and all(x not in data.lower() for x in ['unknown', 'object file', 'cannot import', 'no such file'])
    false_ok = false.get('exit_code') not in (None, 0) and false.get('timed_out') is False and false.get('affinity_mask') == 1 and bool(errors) and all(rfl_error(m) for m in errors) and not any('unparsed' in m for m in fm)
    checks = {'lake_build': success(lake_rec) and len(oleans) == 1, 'unchanged_source_kernel_trust_zero': success(kernel_rec), 'independent_exporter_compiles': success(support), 'actual_universal_type_and_root': success(theorem) and root_audit['status'] == 'PASS', 'all_seven_original_boundary_examples': success(boundary), 'false_conjunction_real_rfl_type_error': false_ok, 'sorry_compiles_but_actual_sorryAx_rejected': success(sorry_rec) and sorry_audit['status'] == 'REJECT' and 'sorryAx' in sorry_audit.get('forbidden_axioms', []), 'custom_axiom_compiles_but_rejected': success(custom_rec) and custom_audit['status'] == 'REJECT' and 'independentForbidden' in custom_audit.get('forbidden_axioms', [])}
    result = {'verdict': 'INDEPENDENT_KERNEL_KNOWN_PROOF_PASS' if all(checks.values()) else 'PARTIAL_OR_FAILED_INDEPENDENT_KERNEL_VALIDATION', 'started_at': started, 'finished_at': now(), 'round_id': args.round_id, 'checks': checks, 'steps': steps, 'actual_root_audit': root_audit, 'sorry_audit': sorry_audit, 'custom_axiom_audit': custom_audit, 'false_control_messages': fm, 'limits': protocol['scope'], 'usd': 0, 'concurrency': 1, 'cpu_affinity_mask': 1, 'replayed': False}
    save(out / 'RESULT.json', result)
    print(json.dumps({'verdict': result['verdict'], 'checks': checks, 'root_audit': root_audit, 'started_at': started, 'finished_at': result['finished_at']}, ensure_ascii=False))
    return 0 if all(checks.values()) else 1

if __name__ == '__main__':
    raise SystemExit(main())
