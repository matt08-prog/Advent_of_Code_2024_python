# from sympy.solvers.diophantine import diophantine
# from sympy import symbols, Eq
# a, b = symbols("a, b", integer=True)
# my_syms = (a, b)
# pythag_eq = 60*a - 45*b - 3000
# # Solve Diophantine equation
# d = diophantine(pythag_eq, syms=my_syms)
# print(d)




# from sympy import symbols, Eq
# from sympy.solvers.diophantine import diophantine

# # x, y, z, p, q = symbols("x y z p q", integer=True)
# a, b, p, q = symbols("a, b, p, q", integer=True)

# eq1 = Eq(94*a + 22*b, 8400)
# eq2 = Eq(34*a + 67*b, 5400)

# sol1 = diophantine(eq1)
# sol2 = diophantine(eq2)

# print("Parameterized solutions for eq1:", sol1)
# print("Parameterized solutions for eq2:", sol2)

# # Find common solutions by substituting values for parameters
# common_solutions = []
# for p_val in range(-5, 6):
#     for q_val in range(-5, 6):
#         sol1_vals = [expr.subs({p: p_val, q: q_val}) for expr in list(sol1)[0]]
#         sol2_vals = [expr.subs({p: p_val}) for expr in list(sol2)[0]]
        
#         if sol1_vals == sol2_vals:
#             common_solutions.append(tuple(sol1_vals))

# print("Common solutions:", common_solutions)


from sympy import Point, Line

res_1 = 8400+10000000000000
res_2 = 5400+10000000000000

p1 = Point(0, res_1/22)  # Point on first line

p2 = Point(res_1/94, 0)  # Another point on first line

p3 = Point(0, res_2/67)  # Point on second line

p4 = Point(res_2/34, 0)  # Another point on second line



line1 = Line(p1, p2)  # Create first line

line2 = Line(p3, p4)  # Create second line



intersection_point = line1.intersection(line2)  # Find intersection

print(int(intersection_point[0][0]))  # Output: [Point2D(1, 1)]