from dis import dis


def print_bytecode(c):
    print(c)
    print(dis(c))
    print()

# basic expression
expr = "min(300, 340, 500)"
print_bytecode(expr)


# Assignment
simple_assignment = "a = x + 100"
print_bytecode(simple_assignment)

# Value swap
assignment = "a, b = b, a"
print_bytecode(assignment)

# Lambda
l = lambda x: x ** 2
print_bytecode(l)
