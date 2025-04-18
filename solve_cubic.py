import sys
import math

def solve_linear(c, d):
    """Solve linear equation cx + d = 0."""
    if abs(c) < 1e-10:
        return [] if abs(d) > 1e-10 else [float('inf')]
    return [-d / c]

def solve_quadratic(b, c, d):
    """Solve quadratic equation bx^2 + cx + d = 0."""
    if abs(b) < 1e-10:
        return solve_linear(c, d)
    discriminant = c**2 - 4*b*d
    if discriminant < 0:
        return []
    elif abs(discriminant) < 1e-10:
        return [-c / (2*b)]
    sqrt_d = math.sqrt(discriminant)
    return [(-c + sqrt_d) / (2*b), (-c - sqrt_d) / (2*b)]

def main():
    # Parse coefficients
    try:
        coeffs = [float(arg) for arg in sys.argv[1:]]
        a, b, c, d = coeffs
    except ValueError:
        print("Ошибка: все аргументы должны быть вещественными числами.", file=sys.stderr)
        sys.exit(1)
        
    if a == 0:
        roots = solve_quadratic(b, c, d)
        if roots == [float('inf')]:
            print("Бесконечное множество решений.", file=sys.stdout)
            sys.exit(0)
        for root in roots:
            print(f"{root:.3f}")
    else:
        print("Решение кубического уравнения")
        
if __name__ == "__main__":
    main()