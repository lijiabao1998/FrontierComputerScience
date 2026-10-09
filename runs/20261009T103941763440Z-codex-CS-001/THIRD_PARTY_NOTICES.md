# Third-party notices

- `vendor/VerifiedCompiler.lean`, `lakefile.toml`, `lake-manifest.json`, and `lean-toolchain` are verbatim from Marcus Rossel’s verified-compiler, commit `4c79694f5b96c6789b307e2911088af6b19540ac`. The original snapshot has no license file. Commit `68a087914c9401bab8742e5f8d236c16dabc485b` adds the MIT license and changes no source or toolchain files; that full license is included alongside the source. Source identity was verified with `git diff` and SHA-256. No legal conclusion beyond this explicit provenance is implied.
- VeriSoftBench evaluation code: MIT, copyright 2026 VeriSoftBench Authors. Only task metadata is recorded, with benchmark commit `f142b4b22c55e3209ec52660b0c857ae533c7533`. No JSONL ground-truth proof field is redistributed or used as a held-out candidate. Upstream source proof is deliberately included for known-proof reproduction.
- Lean 4 official toolchain: Apache-2.0; runtime not redistributed. Official binary retrieval did not complete; no compiler execution is claimed.
- Papers are referenced by links, not republished.

Sources: https://github.com/marcusrossel/verified-compiler/commit/68a087914c9401bab8742e5f8d236c16dabc485b ; https://github.com/utopia-group/VeriSoftBench/blob/f142b4b22c55e3209ec52660b0c857ae533c7533/THIRD_PARTY_NOTICES.txt
