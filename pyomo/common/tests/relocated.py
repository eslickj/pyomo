#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2025
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________
#

from pyomo.common.deprecation import relocated_module_attribute


class Bar(object):
    data = 42


def __getattr__(name):
    if name.startswith('Foo'):
        return name[3:]
    raise AttributeError("module '%s' has no attribute '%s'" % (__name__, name))


relocated_module_attribute('Foo', 'pyomo.common.tests.test_deprecated.Bar', 'test')
relocated_module_attribute('Foo_2', 'pyomo.common.tests.relocated.Bar', 'test')
