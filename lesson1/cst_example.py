import parser
from pprint import pprint
import symbol
import token


tokens = [(t, getattr(token, t)) for t in token.__dict__
          if not t.startswith("_")]
symbols = [(s, getattr(symbol, s)) for s in symbol.__dict__
           if not s.startswith("_")]


def map_st(node):
    """
    node[0] -> token type
    node[1] -> value
    node[1] not list -> leaf node
    """
    token_match = [t[0] for t in tokens if t[1] == node[0]]
    symbol_match = [s[0] for s in symbols if s[1] == node[0]]

    if len(token_match):
        node[0] = token_match[0]
    elif len(symbol_match):
        node[0] = symbol_match[0]

    for child in node[1:]:
        if isinstance(child, list):
            map_st(child)

    return node


expr = "max(100, 200, 500)"
cst = parser.expr(expr).tolist()

print("CST:")
pprint(cst)

print("CST with symbol named:")
pprint(map_st(cst))
