import Lean
import VerifiedCompiler

open Lean Elab Command

namespace IndependentAudit

def constants : Expr → Array Name
  | .const n _ => #[n]
  | .app f a => constants f ++ constants a
  | .lam _ t b _ => constants t ++ constants b
  | .forallE _ t b _ => constants t ++ constants b
  | .letE _ t v b _ => constants t ++ constants v ++ constants b
  | .mdata _ e => constants e
  | .proj _ _ e => constants e
  | _ => #[]

def unique (xs : Array Name) : Array Name :=
  xs.foldl (fun acc n => if acc.contains n then acc else acc.push n) #[]

def category : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"

def namesJson (ns : Array Name) : Json := Json.arr (ns.map (fun n => toJson n.toString))

elab "#cs_audit " root:ident output:str : command => do
  let env ← getEnv
  let rootName := root.getId
  let mut queue := #[rootName]
  let mut at := 0
  let mut seen : NameSet := {}
  let mut nodes : Array Json := #[]
  let mut missing : Array Name := #[]
  while at < queue.size do
    if queue.size > 200000 || nodes.size + missing.size > 20000 then
      throwError "Independent closure cap exceeded; verdict must be PARTIAL"
    let name := queue[at]!
    at := at + 1
    if !seen.contains name then
      seen := seen.insert name
      match env.find? name with
      | none => missing := missing.push name
      | some ci =>
        let tr := unique (constants ci.type)
        let vr := unique (match ci.value? true with | some v => constants v | none => #[])
        queue := queue ++ tr ++ vr
        nodes := nodes.push (Json.mkObj [
          ("name", toJson name.toString), ("kind", toJson (category ci)),
          ("unsafe", toJson ci.isUnsafe), ("partial", toJson ci.isPartial),
          ("has_value", toJson (ci.value? true).isSome),
          ("type_refs", namesJson tr), ("value_refs", namesJson vr)])
  let builtin ← collectAxioms rootName
  let report := Json.mkObj [
    ("schema", toJson "independent-type-value-bfs-v1"),
    ("root", toJson rootName.toString), ("nodes", Json.arr nodes),
    ("missing", namesJson missing), ("processed_queue_entries", toJson at),
    ("builtin_axioms", namesJson builtin), ("opaque_values_included", toJson true),
    ("complete", toJson missing.isEmpty)]
  liftIO (IO.FS.writeFile output.getString (report.compress ++ "\n"))

end IndependentAudit
