import AuditSupport

example : (∀ {τ : Ty} (t : Term τ), Term.Equiv t (Term.constFold t)) := @Term.constFold_equiv
#check Term.constFold_equiv
#print axioms Term.constFold_equiv
#cs_audit Term.constFold_equiv "theorem-closure.json"
