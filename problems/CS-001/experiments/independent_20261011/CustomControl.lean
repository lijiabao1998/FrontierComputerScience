import AuditSupport

axiom independentForbidden : False
theorem forbiddenCustom : False := independentForbidden
#print axioms forbiddenCustom
#cs_audit forbiddenCustom "custom-closure.json"
