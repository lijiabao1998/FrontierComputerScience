import VerifiedCompiler

-- Deliberately unsound diagnostic fixture, never an accepted proof.
theorem forbiddenAdmission : False := by sorry
#print axioms forbiddenAdmission
