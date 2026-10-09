# CS-001 round 1: result and limits

## Outcome

**Proof reproduction blocked; no theorem-verification success is claimed.**

The admitted round prepared an offline, hash-pinned replay of VeriSoftBench task 477 (`Term.constFold_equiv`). All Lean stages are **NOT_RUN** because the official toolchain download did not produce a file and a polling call was cancelled by approval review. The exact tool error and subsequent read-only checks are preserved in `environment_blocker.json`. No alternate download route or paid service was used.

## Completed checks

- Ownership rechecked before claiming issue #3: no conflicting open issue/PR was found. Original repository base is `1688c473bc06bf3b04c40b63b3428ed23443bef6`; governance pin is `9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f`.
- Six fresh queries across four required categories were run after the round began. Exact queries, source URLs, limits, and admission time are in `round.json`.
- Frozen specification hash: `ce1ee55a47b87931a8877f690040ee054c689843e226bd7e76dcf8ebb9b0a6f2`. No protected problem-card fields, existing evaluator, or governance settings changed.
- Source SHA-256 and exact statement checked. Pinned manifest has zero external packages. The source is one module, with zero explicit imports and implicit Lean `Init`. This source inventory is not a compiled declaration closure.
- Twelve Python harness tests pass (including four core/closure classification regressions): empty/permitted axiom reports accepted, admission/custom/native axioms rejected, missing/duplicate target reports rejected, and pinned source inventory checked. A reviewer-identified hazard was fixed: unavailable/failed declaration closure is now PARTIAL with a separate core proof status, never top-level PASS. These are parser/harness tests only.
- Offline runner dry-runs correctly return status NOT_RUN and exit 2 when no existing toolchain is supplied. No Lean trial was attempted.

## Literature update

The original VeriSoftBench v2 study defines its curated context as oracle-like and describes the full 500-task and 100-task compatibility settings as different. It does not establish broad repository-scale synthesis. Its data are public and training contamination cannot be excluded. Source: https://arxiv.org/html/2602.18307v2

The newer October 2026 FORALL-LEAN-AGENT paper reports 100-task subset acceptance, but its original appendix identifies inherited disallowed axioms and a smaller independent-checker coverage set. Those results were read, not independently reproduced here, and do not close CS-001. Source: https://arxiv.org/html/2610.00885v1

No formal retraction/correction was identified in the bounded searches. This is not a guarantee that none exists.

## Leakage and licenses

The selected upstream proof was deliberately viewed and vendored as a known-proof reproduction. No held-out generation, success rate, or novelty claim is made. The JSONL parser printed only allowlisted task metadata and statements, never its ground-truth proof field. Search results exposed some unrelated public proof snippets; these are also a reason not to claim hidden-answer isolation. Benchmark dependency metadata (12 transitive dependencies, depth 3) is labeled upstream-reported and not locally reproduced.

The source pin predates its MIT license file. The later license-only commit leaves source and toolchain unchanged; the full license and explicit provenance are included. See `THIRD_PARTY_NOTICES.md`.

## Reproduction and next smallest step

From `problems/CS-001/experiments/lean-baseline-r1`, run `python3 -m unittest -v test_reproduce.py`; then supply an existing official Lean 4.18.0 distribution to `python3 reproduce.py --output /tmp/cs001-replay --toolchain-dir /path/to/lean-4.18.0-linux`. The runner preserves stdout/stderr, return codes, versions and hashes and never downloads anything.

Before claiming success, a later authorized round must actually build the source, audit target axioms, compile all seven boundary checks, reject the false theorem, reject the admitted fixture through its axiom report, and measure the declaration closure. The Lean probe syntax is currently uncompiled. An independent reviewer must distinguish artifact audit from independent proof verification.

The parent problem remains OPEN. No main write, merge, paid API, GPU, credentials, or user computer was used.

## Independent artifact review

A separate session verified source identity and independently exercised absent/nonexistent-toolchain and tampered-source cases. The raw report is `independent_harness_review.json`. It certifies only offline guard behavior; formal proof and semantic dependency closure remain NOT_RUN. Its closure-status concern was fixed and regression-tested, with response in `review_response.json`.
