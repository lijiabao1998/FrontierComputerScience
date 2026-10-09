import Lean
import VerifiedCompiler

open Lean Elab Command

-- Observational transitive closure of all referenced types and values.
-- Generated declarations are retained. This is NOT the benchmark's filtered metric.
def baselineClosure (env : Environment) (root : Name) : Array Name := Id.run do
  let mut seen : NameSet := {}
  let mut todo := [root]
  let mut result := #[]
  while !todo.isEmpty do
    match todo with
    | [] => break
    | n :: rest =>
      todo := rest
      if seen.contains n then continue
      seen := seen.insert n
      match env.find? n with
      | none => continue
      | some info =>
        result := result.push n
        for c in info.type.getUsedConstants do
          if !seen.contains c then todo := c :: todo
        match info.value? with
        | none => pure ()
        | some v =>
          for c in v.getUsedConstants do
            if !seen.contains c then todo := c :: todo
  return result

run_cmd do
  let env ← getEnv
  let deps := baselineClosure env `Term.constFold_equiv
  for n in deps do
    let moduleName := match env.getModuleIdxFor? n with
      | none => "CURRENT_OR_UNKNOWN"
      | some idx => env.allImportedModuleNames[idx.toNat]!.toString
    logInfo m!"DEPENDENCY\t{moduleName}\t{n}"
  logInfo m!"DECLARATION_CLOSURE_WITH_ROOT_AND_GENERATED\t{deps.size}"
