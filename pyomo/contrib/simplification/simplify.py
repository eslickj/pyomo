#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2024
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

from pyomo.core.expr.sympy_tools import sympy2pyomo_expression, sympyify_expression
from pyomo.core.expr.numeric_expr import NumericExpression
from pyomo.core.expr.numvalue import value, is_constant
import logging
import warnings

from pyomo.contrib.simplification.ginac import (
    interface as ginac_interface,
    interface_available as ginac_available,
)

logger = logging.getLogger(__name__)


def simplify_with_sympy(expr: NumericExpression):
    if is_constant(expr):
        return value(expr)
    om, se = sympyify_expression(expr)
    se = se.simplify()
    new_expr = sympy2pyomo_expression(se, om)
    if is_constant(new_expr):
        new_expr = value(new_expr)
    return new_expr


def simplify_with_ginac(expr: NumericExpression, ginac_interface):
    if is_constant(expr):
        return value(expr)
    gi = ginac_interface
    ginac_expr = gi.to_ginac(expr)
    ginac_expr = ginac_expr.normal()
    new_expr = gi.from_ginac(ginac_expr)
    return new_expr


class Simplifier(object):
    def __init__(self, suppress_no_ginac_warnings: bool = False) -> None:
        if ginac_available:
            self.gi = ginac_interface.GinacInterface(False)
        self.suppress_no_ginac_warnings = suppress_no_ginac_warnings

    def simplify(self, expr: NumericExpression):
        if ginac_available:
            return simplify_with_ginac(expr, self.gi)
        else:
            if not self.suppress_no_ginac_warnings:
                msg = (
                    "GiNaC does not seem to be available. Using SymPy. "
                    + "Note that the GiNac interface is significantly faster."
                )
                logger.warning(msg)
                warnings.warn(msg)
                self.suppress_no_ginac_warnings = True
            return simplify_with_sympy(expr)
