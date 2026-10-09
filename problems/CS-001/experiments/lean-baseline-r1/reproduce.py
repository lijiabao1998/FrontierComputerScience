#!/usr/bin/env python3
"""Offline-only, pinned known-proof replay. Never installs or downloads tools.

Usage: python reproduce.py --output /tmp/cs001-result [--toolchain-dir /path/to/lean-4.18.0-linux]
Exit 0 = core proof + closure pass; 1 = core failure; 2 = proof NOT_RUN; 3 = core pass, closure unavailable.
The script is a reproduction harness, not a general adversarial proof evaluator.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
TARGET = 'Term.constFold_equiv'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
SOURCE_HASH = '2454c074170e8f2ca8e05b1339678457a5873a50307d4e2c1e1c1e585ca02a85'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_axioms(output, target=TARGET):
    """Require exactly one target axiom report; ignore unrelated diagnostics."""
    plain = re.findall(r"^'" + re.escape(target) + r"' does not depend on any axioms\s*$", output, re.M)
    reports = re.findall(r"^'" + re.escape(target) + r"' depends on axioms:\s*\[([^\]]*)\]", output, re.M)
    if len(plain) + len(reports) != 1:
        raise ValueError('missing or ambiguous axiom report for exact target')
    if plain:
        return set()
    return {x.strip() for x in reports[0].split(',') if x.strip()}


def classify_replay(core_ok, closure_status):
    # Closure is conditional in the frozen spec, but never hide its absence in PASS.
    if not core_ok:
        return 'FAIL', 1
    if closure_status == 'PASS':
        return 'PASS', 0
    return 'PARTIAL', 3


def source_inventory():
    manifest = json.loads((HERE / 'source_manifest.json').read_text())
    actual = {n: sha256(HERE / 'vendor' / n) for n in manifest['files']}
    if actual != manifest['files'] or actual['VerifiedCompiler.lean'] != SOURCE_HASH:
        raise ValueError('frozen source hash mismatch')
    source = (HERE / 'vendor/VerifiedCompiler.lean').read_text()
    if 'theorem constFold_equiv (t : Term τ) : t ~ constFold t := by' not in source:
        raise ValueError('exact source theorem statement missing')
    if re.search(r'\b(sorry|admit|axiom|native_decide)\b', source):
        raise ValueError('unexpected escape token in pinned source')
    packages = json.loads((HERE / 'vendor/lake-manifest.json').read_text())['packages']
    imports = re.findall(r'^import\s+(.+)$', source, re.M)
    return {'status': 'PASS', 'files_sha256': actual,
            'source_modules': ['VerifiedCompiler'], 'explicit_imports': imports,
            'implicit_core_import': 'Init', 'external_lake_packages': packages,
            'module_inventory_method': 'Exact pinned source import lines and Lake manifest; not compiled environment introspection.',
            'transitive_declaration_closure': 'Not measured by source inventory; see declaration_closure. Benchmark metadata count is not a measurement here.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--toolchain-dir', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    result = {'kind': 'KNOWN_PROOF_REPRODUCTION', 'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'status': 'NOT_RUN', 'core_proof_status': 'NOT_RUN', 'paid_cost_usd': 0, 'random_seed': None,
              'seed_reason': 'Deterministic pinned source replay; no sampling.',
              'environment': {'python': platform.python_version(), 'platform': platform.platform(), 'machine': platform.machine()},
              'commands': [], 'declaration_closure': {'status': 'NOT_RUN'}, 'claims': {'held_out_success': False, 'novel_proof': False, 'parent_completed': False,
                                        'independent_alternate_kernel': 'NOT_RUN'}, 'stages': {}}
    def finish(code, reason):
        result['reason'] = reason
        result['finished_at'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'status': result['status'], 'reason': reason, 'result': str(out / 'result.json')}))
        return code
    try:
        result['stages']['source_inventory'] = source_inventory()
    except (ValueError, OSError, KeyError) as e:
        result['status'] = 'FAIL'
        return finish(1, str(e))
    for stage in ['repository_build', 'target_axiom_audit', 'boundary_cases', 'false_theorem_rejection', 'sorry_control_rejection']:
        result['stages'][stage] = {'status': 'NOT_RUN'}
    if args.toolchain_dir is None:
        return finish(2, 'No explicit existing toolchain supplied. This offline runner never installs or downloads Lean.')
    tc = args.toolchain_dir.resolve()
    lean, lake = tc / 'bin/lean', tc / 'bin/lake'
    if not lean.is_file() or not lake.is_file():
        return finish(2, 'Explicit toolchain directory lacks bin/lean or bin/lake.')
    # The provided directory must be a real distribution, not elan shims.
    if not (tc / 'lib/lean/Init.olean').is_file():
        return finish(2, 'Explicit directory lacks compiled Init.olean; refusing automatic toolchain resolution.')
    env = dict(os.environ)
    env['PATH'] = str(tc / 'bin') + os.pathsep + env.get('PATH', '')
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'ELAN_TOOLCHAIN']:
        env.pop(key, None)
    cpus = sorted(os.sched_getaffinity(0))[:2] if hasattr(os, 'sched_getaffinity') else None
    result['environment']['cpu_affinity'] = cpus
    def restrict_cpu():
        if cpus:
            os.sched_setaffinity(0, cpus)
    def run(label, argv, cwd):
        started = time.monotonic()
        try:
            p = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True,
                               timeout=120, preexec_fn=restrict_cpu if cpus else None)
            code, stdout, stderr = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            code = 124
            stdout = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or '')
            stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or '')
            stderr += '\nTIMEOUT after 120 seconds'
        (out / (label + '.stdout.txt')).write_text(stdout)
        (out / (label + '.stderr.txt')).write_text(stderr)
        record = {'label': label, 'argv': [str(a) for a in argv], 'returncode': code,
                  'wall_seconds': time.monotonic() - started, 'stdout_sha256': sha256(out / (label + '.stdout.txt')),
                  'stderr_sha256': sha256(out / (label + '.stderr.txt'))}
        result['commands'].append(record)
        return code, stdout + '\n' + stderr
    with tempfile.TemporaryDirectory(prefix='cs001-replay-') as tmp:
        work = Path(tmp)
        for p in (HERE / 'vendor').iterdir():
            shutil.copyfile(p, work / p.name)
        for name in ['Audit.lean', 'Boundary.lean', 'FalseControl.lean', 'SorryControl.lean', 'Closure.lean']:
            shutil.copyfile(HERE / name, work / name)
        code, version = run('lean-version', [lean, '--version'], work)
        result['environment']['lean_version'] = version.strip()
        result['environment']['lean_binary_sha256'] = sha256(lean)
        if code or not re.search(r'\bversion 4\.18\.0(?:,|\s)', version):
            result['status'] = 'FAIL'
            return finish(1, 'Toolchain is not pinned Lean 4.18.0.')
        code, output = run('repository-build', [lake, 'build'], work)
        result['stages']['repository_build'] = {'status': 'PASS' if code == 0 else 'FAIL'}
        if code:
            result['status'] = 'FAIL'
            return finish(1, 'Unmodified repository build failed; dependent proof probes not run.')
        code, output = run('target-axiom-audit', [lake, 'env', 'lean', 'Audit.lean'], work)
        try:
            axioms = parse_axioms(output)
            audit_ok = code == 0 and axioms <= ALLOWED
            result['stages']['target_axiom_audit'] = {'status': 'PASS' if audit_ok else 'FAIL', 'axioms': sorted(axioms)}
        except ValueError as e:
            result['stages']['target_axiom_audit'] = {'status': 'FAIL', 'reason': str(e)}
        code, output = run('boundary-cases', [lake, 'env', 'lean', 'Boundary.lean'], work)
        result['stages']['boundary_cases'] = {'status': 'PASS' if code == 0 else 'FAIL', 'cases': 7}
        code, output = run('false-theorem', [lake, 'env', 'lean', 'FalseControl.lean'], work)
        false_ok = code not in (0, 124) and 'error:' in output and "tactic 'rfl' failed" in output
        result['stages']['false_theorem_rejection'] = {'status': 'PASS' if false_ok else 'FAIL', 'compiler_returncode': code}
        code, output = run('sorry-control', [lake, 'env', 'lean', 'SorryControl.lean'], work)
        try:
            axioms = parse_axioms(output, 'forbiddenAdmission')
            reject_ok = code == 0 and 'sorryAx' in axioms and not axioms <= ALLOWED
            result['stages']['sorry_control_rejection'] = {'status': 'PASS' if reject_ok else 'FAIL', 'axioms': sorted(axioms),
                                                       'note': 'Lean accepts the admitted fixture; the explicit axiom rule must reject it.'}
        except ValueError as e:
            result['stages']['sorry_control_rejection'] = {'status': 'FAIL', 'reason': str(e)}
        code, output = run('declaration-closure', [lake, 'env', 'lean', 'Closure.lean'], work)
        dependency_lines = [line for line in output.splitlines() if line.startswith('DEPENDENCY\t')]
        result['declaration_closure'] = {'status': 'PASS' if code == 0 and dependency_lines else 'FAIL',
                                         'count_including_target_and_generated': len(dependency_lines),
                                         'method': 'Transitively walk ConstantInfo type and value constants, including core and generated declarations. Not comparable to filtered benchmark count.'}
        all_ok = all(s['status'] == 'PASS' for s in result['stages'].values())
        result['core_proof_status'] = 'PASS' if all_ok else 'FAIL'
        result['status'], exit_code = classify_replay(all_ok, result['declaration_closure']['status'])
        return finish(exit_code, 'Core proof controls and declaration closure are reported separately; no synthesis or generality claim.')


if __name__ == '__main__':
    raise SystemExit(main())
