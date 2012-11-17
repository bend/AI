"""Helper module to call minisat."""

import os
import tempfile


def minisat(n, clauses, executable="./minisat"):
    """Run Minisat on the given set of clauses. Return None if the clauses are
    unsatisfiable, or a solution that satisfies all the clauses (a sequence of
    integers representing the variables that are true).

    Arguments:
    n -- number of variables (each variable is denoted by an integer within the
        range 1..n)
    clauses -- sequence of clauses. Each clause is a tuple of integers
        representing the literals: a positive integer for a variable, a
        negative integer for the negated variable.
    executable -- name of the MiniSat executable to run

    Example:
    Consider a vocabulary with 3 variables A, B, C and the clauses !A || B,
    !B || !C and A.

    >>> minisat(3, [(-1, 2), (-2, -3), (1,)])
    [1, 2]

    meaning the clauses are satisfiable and {A=True, B=True, C=False} is a
    model."""
    clausesfile = None
    solfile = None
    try:
        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            clausesfile = f.name
            print("p cnf", n, len(clauses), file=f)
            for c in clauses:
                print(" ".join(str(l) for l in c), "0", file=f)
        with tempfile.NamedTemporaryFile() as f:
            solfile = f.name
        os.system("%s %s %s" % (executable, clausesfile, solfile))
        with open(solfile) as f:
            if f.readline().strip() == "UNSAT":
                return None
            else:
                return [int(x) for x in f.readline().strip().split(" ")
                               if int(x) > 0]
    finally:
        try:
            if clausesfile is not None:
                os.remove(clausesfile)
            if solfile is not None:
                os.remove(solfile)
        except:
            pass
