from formula_creator import FormulaCreator

# 1. Define a new Formula creator
f = FormulaCreator('Mass', 'm', 'g')

# 2. Create all quantities
I = f.create_quantity("Current", "I")
t = f.create_quantity("Time", "t")

# 3. Create all constants
c_F = 96500.00
c_A = 63.50
c_n = 2

# 4. Create an expression
formula = c_A / (c_F * c_n) * I * t

# 5. Set expression as formula
f.set_formula(formula)

# 6. Set values for all quantities
f.set_values_and_uncertainties({
    I: (0.5, 0.5 * 0.75 / 100),
    t: (30 * 60, 0.3)
})

# 7. Get results
results = f.calculate()
f.set_print_options(3)
print(results)