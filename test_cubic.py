import unittest
import subprocess
import sys
from solve_cubic import solve_cubic

class TestCubicSolver(unittest.TestCase):
    def assertRootsEqual(self, actual, expected, delta=1e-6):
        """Compare lists of roots with tolerance."""
        self.assertEqual(len(actual), len(expected))
        for a, e in zip(sorted(actual), sorted(expected)):
            self.assertAlmostEqual(a, e, delta=delta)

    def test_solve_cubic_three_roots(self):
        # x^3 - 6x^2 + 11x - 6 = 0 (roots: 1, 2, 3)
        self.assertRootsEqual(solve_cubic(1, -6, 11, -6), [1.0, 2.0, 3.0])
        # Same equation with scaled coefficients: -x^3 + 6x^2 - 11x + 6 = 0
        self.assertRootsEqual(solve_cubic(-1, 6, -11, 6), [1.0, 2.0, 3.0])
        # Same equation with different scaling: -0.5x^3 + 3x^2 - 5.5x + 3 = 0
        self.assertRootsEqual(solve_cubic(-0.5, 3, -5.5, 3), [1.0, 2.0, 3.0])
        
    def test_solve_cubic_double_root(self):
        # x^3 - 2x^2 + x = 0 (roots: 0, 1, 1)
        self.assertRootsEqual(solve_cubic(1, -2, 1, 0), [0.0, 1.0])
        
    def test_solve_cubic_one_root(self):
        # x^3 + 1 = 0 (root: -1)
        self.assertRootsEqual(solve_cubic(1, 0, 0, 1), [-1.0])

    def test_solve_cubic_quadratic(self):
        # x^2 + 2x + 1 = 0 (root: -1)
        self.assertRootsEqual(solve_cubic(0, 1, 2, 1), [-1.0])
        # x^2 - 1 = 0 (roots: -1, 1)
        self.assertRootsEqual(solve_cubic(0, 1, 0, -1), [-1.0, 1.0])
        
    def test_solve_cubic_linear(self):
        # 2x + 4 = 0 (root: -2)
        self.assertRootsEqual(solve_cubic(0, 0, 2, 4), [-2.0])

    def test_solve_cubic_no_roots(self):
        # Constant non-zero: no roots
        self.assertRootsEqual(solve_cubic(0, 0, 0, 1), [])

    def test_solve_cubic_infinite(self):
        # All zero: infinite solutions
        self.assertRootsEqual(solve_cubic(0, 0, 0, 0), [float('inf')])
        
    def test_eps_threshold(self):
        # Threshold value: a = 0 -> x^2 - 1 = 0 (root: -1, 1)
        self.assertRootsEqual(solve_cubic(1e-12, 1, 0, -1), [-1.0, 1.0])
        # Threshold value: a = 0, b = 0 -> x - 6 = 0 (root: 6)
        self.assertRootsEqual(solve_cubic(1e-12, 1e-11, 1, -6), [6.0])
    
    def test_very_large_values(self):
        # (x^3 - 6x^2 + 11x - 6) * 1e12 = 0 (roots: 1, 2, 3)
        self.assertRootsEqual(solve_cubic(1e12, -6e12, 11e12, -6e12), [1.0, 2.0, 3.0])
        
    def test_cli_three_roots(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "1", "-6", "11", "-6"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "1 2 3")
        self.assertEqual(result.stderr, "")

        # Same equation with different coefficients
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "-1", "6", "-11", "6"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "1 2 3")
        self.assertEqual(result.stderr, "")

        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "-0.5", "3", "-5.5", "3"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "1 2 3")
        self.assertEqual(result.stderr, "")
        
    def test_cli_double_root(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "1", "-2", "1", "0"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "0 1")
        self.assertEqual(result.stderr, "")

    def test_cli_one_root(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "1", "0", "0", "1"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "-1")
        self.assertEqual(result.stderr, "")
        
    def test_cli_quadratic(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "0", "1", "2", "1"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "-1")
        self.assertEqual(result.stderr, "")

    def test_cli_no_roots(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "0", "0", "0", "1"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "x ∈ ∅")
        self.assertEqual(result.stderr, "")

    def test_cli_infinite_solutions(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "0", "0", "0", "0"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "x ∈ ℝ")
        self.assertEqual(result.stderr, "")

    def test_cli_invalid_args_count(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "1", "2"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ошибка: требуется 4 коэффициента", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_cli_invalid_args_type(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "1", "a", "3", "4"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ошибка: все аргументы должны быть вещественными числами", result.stderr)
        self.assertEqual(result.stdout, "")
        
    def test_cli_help(self):
        result = subprocess.run(
            [sys.executable, "solve_cubic.py", "help"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Использование", result.stdout)
        
if __name__ == "__main__":
    unittest.main()