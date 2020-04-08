"""
Exercise:

Replace assert statements with a comparison condition between two terms
(e.g. assert a == b) with a call to a function that takes a, b and an
operator function as arguments and that runs the assertion printing a more
descriptive message.
"""
import ast
from operator import eq, ne, gt, ge, lt, le


def assert_(a, op, b):
    """
    Assert op(a, b) with a more descriptive error message.

    Args:
        a (object):
        op (callable): Function that takes two arguments and returns
            a boolean. Should be used with functions from the operator
            module.
        b (object):
    """
    assertion_result = op(a, b)

    message = f"where left = {a} and right = {b}"

    assert assertion_result, message


# Maps AST node types to functions
OP_MAP = {
    ast.Eq: eq,
    ast.NotEq: ne,
    ast.Gt: gt,
    ast.GtE: ge,
    ast.Lt: lt,
    ast.LtE: le
}


class RewriteAsserts(ast.NodeTransformer):
    def visit_Assert(self, node):
        """
        Visits Assert nodes and change those that test against a Compare
        node to a function call

        Args:
            node (ast.Node):

        Returns:
            Original node if the test is not Compare, Expr node otherwise.
        """
        # We only look at Compare nodes
        if isinstance(node.test, ast.Compare):
            # Get the operator function
            op = OP_MAP[node.test.ops[0].__class__]

            # Construct the call code, with op being the name of the operator
            # function
            call = ast.Call(
                func=ast.Name(id="assert_", ctx=ast.Load()),
                args=[
                    node.test.left,
                    ast.Name(id=op.__name__, ctx=ast.Load()),
                    node.test.comparators[0]
                ],
                keywords=[]
            )

            # Wrap the call in an Expr
            new_node = ast.Expr(value=call)

            # Copy and fix locations on the new node
            ast.copy_location(new_node, node)
            ast.fix_missing_locations(new_node)

            return new_node

        return node


def exec_ast(as_tree, globals=None, locals=None):
    """
    Compiles and executes the code of an AST (ast.Node) in a given context,
    through globals and locals. If globals and locals are None, the context
    of this function's body is used.

    Args:
        as_tree (ast.Node): AST
    """
    # Compile
    code_obj = compile(as_tree, "<string>", "exec")
    exec(code_obj, globals, locals)


# This function takes two parameters a and b, prints them out, and then
# asserts that they are equal
func_str = """
def func(a, b):
    print(a, b)

    assert a == b
"""

func_ast = ast.parse(func_str)
print(f"AST for func: {ast.dump(func_ast)}\n")

transformed_func_ast = RewriteAsserts().visit(func_ast)
print(f"Modified AST for func: {ast.dump(transformed_func_ast)}\n")

# Compile function in current context
exec_ast(transformed_func_ast, globals(), locals())


# Now func is available and compiled
# This should just print 10, 10
func(10, 10)

# This should print 20, 50 and raise an AssertionError with a pretty message
func(20, 50)
