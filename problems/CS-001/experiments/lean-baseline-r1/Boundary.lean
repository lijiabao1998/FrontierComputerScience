import VerifiedCompiler

-- Four boolean inputs, zero natural, and both conditional branches.
example : Term.eval (Term.constFold (.and (.val (.bool true)) (.val (.bool true)))) = .bool true := rfl
example : Term.eval (Term.constFold (.and (.val (.bool true)) (.val (.bool false)))) = .bool false := rfl
example : Term.eval (Term.constFold (.and (.val (.bool false)) (.val (.bool true)))) = .bool false := rfl
example : Term.eval (Term.constFold (.and (.val (.bool false)) (.val (.bool false)))) = .bool false := rfl
example : Term.eval (Term.constFold (.val (.nat 0))) = .nat 0 := rfl
example : Term.eval (Term.constFold (.ite (.val (.bool true)) (.val (.nat 0)) (.val (.nat 1)))) = .nat 0 := rfl
example : Term.eval (Term.constFold (.ite (.val (.bool false)) (.val (.nat 0)) (.val (.nat 1)))) = .nat 1 := rfl
