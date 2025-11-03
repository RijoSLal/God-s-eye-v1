from tree_sitter_language_pack import get_language
from tree_sitter import Parser



lang = get_language("python")


parse = Parser(language = lang)

code = """
import os
import sys
from math import sqrt, sin

print(os.name)
"""
tree = parse.parse(bytes(code, "utf8"))
root = tree.root_node

print(root.type)


