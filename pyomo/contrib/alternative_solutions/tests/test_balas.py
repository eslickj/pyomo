import pytest
from numpy.testing import assert_array_almost_equal
from collections import Counter

import pyomo.environ as pe
import pyomo.common.unittest as unittest
import pyomo.opt

from pyomo.contrib.alternative_solutions import enumerate_binary_solutions
import pyomo.contrib.alternative_solutions.tests.test_cases as tc


solvers = list(pyomo.opt.check_available_solvers("glpk", "gurobi", "appsi_gurobi"))
pytestmark = pytest.mark.parametrize("mip_solver", solvers)


@unittest.pytest.mark.default
class TestBalasUnit:

    def test_ip_feasibility(self, mip_solver):
        """
        Enumerate solutions for an ip: triangle_ip.

        Check that there is just one solution when the # of binary variables is 0.
        """
        m = tc.get_triangle_ip()
        results = enumerate_binary_solutions(m, num_solutions=100, solver=mip_solver)
        assert len(results) == 1
        assert results[0].objective_value == pytest.approx(5)

    def test_no_time(self, mip_solver):
        """
        Enumerate solutions for an ip: triangle_ip.

        Check that something sensible happens when the solver times out.
        """
        m = tc.get_triangle_ip()
        with pytest.raises(Exception):
            results = enumerate_binary_solutions(
                m, num_solutions=100, solver=mip_solver, solver_options={"TimeLimit": 0}
            )

    def test_knapsack_all(self, mip_solver):
        """
        Enumerate solutions for a binary problem: knapsack

        """
        m = tc.get_aos_test_knapsack(
            1, weights=[3, 4, 6, 5], values=[2, 3, 1, 4], capacity=8
        )
        results = enumerate_binary_solutions(m, num_solutions=100, solver=mip_solver)
        objectives = list(
            sorted((round(result.objective[1], 2) for result in results), reverse=True)
        )
        assert_array_almost_equal(objectives, m.ranked_solution_values)
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, m.num_ranked_solns)

    def test_knapsack_x0_x1(self, mip_solver):
        """
        Enumerate solutions for a binary problem: knapsack

        Check that we only see 4 solutions that enumerate alternatives of x[1] and x[1]
        """
        m = tc.get_aos_test_knapsack(
            1, weights=[3, 4, 6, 5], values=[2, 3, 1, 4], capacity=8
        )
        results = enumerate_binary_solutions(
            m, num_solutions=100, solver=mip_solver, variables=[m.x[0], m.x[1]]
        )
        objectives = list(
            sorted((round(result.objective[1], 2) for result in results), reverse=True)
        )
        assert_array_almost_equal(objectives, [6, 5, 4, 3])
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, [1, 1, 1, 1])

    def test_knapsack_optimal_3(self, mip_solver):
        """
        Enumerate solutions for a binary problem: knapsack

        """
        m = tc.get_aos_test_knapsack(
            1, weights=[3, 4, 6, 5], values=[2, 3, 1, 4], capacity=8
        )
        results = enumerate_binary_solutions(m, num_solutions=3, solver=mip_solver)
        objectives = list(
            sorted((round(result.objective[1], 2) for result in results), reverse=True)
        )
        assert_array_almost_equal(objectives, m.ranked_solution_values[:3])

    def test_knapsack_hamming_3(self, mip_solver):
        """
        Enumerate solutions for a binary problem: knapsack

        """
        m = tc.get_aos_test_knapsack(
            1, weights=[3, 4, 6, 5], values=[2, 3, 1, 4], capacity=8
        )
        results = enumerate_binary_solutions(
            m, num_solutions=3, solver=mip_solver, search_mode="hamming"
        )
        objectives = list(
            sorted((round(result.objective[1], 2) for result in results), reverse=True)
        )
        assert_array_almost_equal(objectives, [6, 3, 1])

    def test_knapsack_random_3(self, mip_solver):
        """
        Enumerate solutions for a binary problem: knapsack

        """
        m = tc.get_aos_test_knapsack(
            1, weights=[3, 4, 6, 5], values=[2, 3, 1, 4], capacity=8
        )
        results = enumerate_binary_solutions(
            m,
            num_solutions=3,
            solver=mip_solver,
            search_mode="random",
            seed=1118798374,
        )
        objectives = list(
            sorted((round(result.objective[1], 2) for result in results), reverse=True)
        )
        assert_array_almost_equal(objectives, [6, 5, 4])


if __name__ == "__main__":
    unittest.main()
