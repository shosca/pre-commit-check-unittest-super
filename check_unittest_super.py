#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
from functools import partial
import optparse
import sys


class TestSuperChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = 0
        self.current_filename = ""

    def check_files(self, files):
        for file in files:
            self.check_file(file)

    def check_file(self, filename):
        self.current_filename = filename
        try:
            with open(filename, "rb") as fd:
                tree = ast.parse(fd.read(), filename=filename)

            self.visit(tree)
        except SyntaxError as error:
            print("SyntaxError on file %s:%d" % (filename, error.lineno))

    def visit_FunctionDef(self, node):
        if node.name in ["setUp", "tearDown", "setUpClass", "tearDownClass"]:
            is_super_present = any(self.find_super_in_expression(node, i) for i in node.body)
            if not is_super_present:
                print(
                    "{}:{} you may have not called super in {} method"
                    "".format(self.current_filename, node.lineno, node.name)
                )
            self.errors += int(not is_super_present)

    def find_super_in_expression(self, func, expr):
        try:
            super_call = expr.value.func.value.func.id
            called_attr = expr.value.func.attr

            return super_call == "super" and called_attr == func.name

        except AttributeError:
            return False


def main():
    parser = optparse.OptionParser(
        usage="%prog [options] file [files]",
        description="Checks that the test file setUp and tearDown contain super() calls",
    )
    opts, files = parser.parse_args()
    if len(files) == 0:
        parser.error("No filenames provided")

    checker = TestSuperChecker()
    checker.check_files(files)
    return 1 if checker.errors else 0


if __name__ == "__main__":
    sys.exit(main())
