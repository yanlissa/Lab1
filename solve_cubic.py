import sys
import math

def solve_linear(c, d):
    """Solve linear equation cx + d = 0."""
    return [-d / c]

def solve_quadratic(b, c, d):
    """Solve quadratic equation bx^2 + cx + d = 0."""
    discriminant = c**2 - 4*b*d
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
        if b == 0:
            if c == 0:
                if d == 0:
                    print("Бесконечное множество решений.", file=sys.stdout)
                    sys.exit(0)
            else:
                x = solve_linear(c, d)
                print (f"{x:.3f}")
        else:
            x1, x2 = solve_quadratic(b, c, d)
            print (f"{x1:.3f}, {x2:.3f}")
    else:
        print("Решение кубического уравнения")
        
if __name__ == "__main__":
    main()