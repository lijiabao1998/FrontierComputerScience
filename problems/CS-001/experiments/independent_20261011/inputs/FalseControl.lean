import VerifiedCompiler

-- Deliberately false: true AND true does not evaluate to false.
example : Term.Equiv (.and (.val (.bool true)) (.val (.bool true))) (.val (.bool false)) := by
  rfl
