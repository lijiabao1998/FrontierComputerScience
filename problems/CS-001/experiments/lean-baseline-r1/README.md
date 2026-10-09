# CS-001: pinned known-proof baseline (round 1)

This is a **known-proof reproduction package**, not a submitted new proof or a held-out prover evaluation. The source proof was deliberately read. The parent CS-001 problem remains OPEN.

## Current result

**Lean stages NOT_RUN.** No Lean/lake installation was available. An official Lean 4.18.0 release download was attempted; polling that command returned `automatic approval review was cancelled`. That action was stopped without retry or an alternate retrieval route. A subsequent read-only check found no matching process and no archive. Do not treat the Python unit tests or source inventory as theorem verification.

The runnable source is VeriSoftBench task 477, `Term.constFold_equiv`, at original repository commit `4c79694f5b96c6789b307e2911088af6b19540ac`. Its unchanged theorem says that restricted constant folding preserves evaluation for every finite term of the original indexed `Term` type.

## Reproduce offline

Use an existing official Lean 4.18.0 distribution. The runner neither installs nor downloads software and does not call any model API.

```sh
python3 -m unittest -v test_reproduce.py
python3 reproduce.py --output /tmp/cs001-replay \
  --toolchain-dir /absolute/path/to/lean-4.18.0-linux
```

Exit codes: 0 = core proof controls and declaration closure pass; 1 = core failure; 2 = required Lean stages NOT_RUN; 3 = core proof controls pass but declaration closure is failed or unavailable. `core_proof_status` and `declaration_closure.status` are separate. Closure absence cannot produce top-level PASS. Every invocation writes `result.json`; real compiler invocations retain stdout, stderr, return code and elapsed time. The runner first checks source hashes and pinned toolchain version, then builds a temporary copy of the unchanged repository.

`Audit.lean` queries the existing theorem and its transitive axiom assumptions. Only `propext`, `Classical.choice`, and `Quot.sound` are permitted. `FalseControl.lean` must fail for the false conjunction claim. `SorryControl.lean` demonstrates why successful compilation is insufficient: Lean may accept it, but the recorded `sorryAx` must violate the axiom rule. `Boundary.lean` checks seven concrete endpoints. `Closure.lean` optionally measures the elaborated declaration closure; it is presently uncompiled and NOT_RUN.

## Dependency meanings

- Source-module inventory: one original `.lean` module, no explicit imports, implicit Lean `Init`.
- Lake package inventory: the pinned manifest contains zero external packages.
- Benchmark metadata: task 477 reports 12 transitive dependencies and nesting depth 3. These are upstream filtered counts, not locally reproduced measurements.
- `Closure.lean`: follows declaration type/value dependencies transitively, retaining generated and core declarations and the target itself. Its counts, if measured later, are intentionally distinct from the benchmark's filtered count.

## Provenance and limits

All `vendor/` files are pinned and hashed in `source_manifest.json`. The original commit predates the MIT license addition; the later license-only commit `68a087914c9401bab8742e5f8d236c16dabc485b` changes no source or toolchain files. Its full license is retained.

This tiny repository is itself described upstream as a toy compiler. Even a future successful replay establishes no general repository-scale synthesis, performance improvement, unseen-repository success, absence of training contamination, or correctness of natural-language specification translation. An alternate independent kernel is not run. The Python runner is a bounded reproduction harness, not a hardened general-purpose evaluator for adversarial submitted code.
