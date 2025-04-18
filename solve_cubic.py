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

def solve_cubic(a, b, c, d):
    """Solve cubic equation ax^3 + bx^2 + cx + d = 0."""
    if abs(a) < 1e-10:
        return solve_quadratic(b, c, d)
    
    # Depressed cubic: y^3 + py + q = 0 via substitution x = y - b/3a
    p = (3 * a * c - b**2) / (3 * a**2)
    q = (2 * b**3 - 9 * a * b * c + 27 * a**2 * d) / (27 * a**3)
    
    # Discriminant for cubic
    discriminant = (q/2)**2 + (p/3)**3
    roots = []
    
    if abs(discriminant) < 1e-10:
        # One real root (double root case)
        if p == 0 and q == 0:
            x = - b / (3 * a)
            roots.append(x)
        else:
            alpha = math.cbrt(-q/2)
            y1 = 2 * alpha
            y2 = - alpha
            x1 = y1 - b / (3 * a)
            x2 = y2 - b / (3 * a)
            roots.append(x1)
            roots.append(x2)
    elif discriminant > 0:
        # One real root (two complex root)
        y = math.cbrt(-q/2 + math.sqrt(discriminant)) + math.cbrt(-q/2 - math.sqrt(discriminant))
        x = y - b/(3 * a)
        roots.append(x)
    else:
        # Three real roots
        phi = math.acos(-q / (2 * math.sqrt((-p/3)**3))) if p < 0 else 0
        for k in range(3):
            t = 2 * math.sqrt(-p/3) * math.cos(phi/3 + 2*math.pi*k/3)
            x = t - b/(3*a)
            roots.append(x)

    roots.sort()
    return roots

def print_help():
    """Print help message to stdout."""
    print("Программа решает кубическое уравнение ax^3 + bx^2 + cx + d = 0.")
    print("Использование: solve_cubic a b c d")
    print("  a, b, c, d - вещественные коэффициенты (например, 1 -2 1 0).")
    print("  help       - вывод этой справки.")
    print("Вывод: действительные корни в одной строке, разделенные пробелами. Целые числа без десятичной части, нецелые — с точностью до 3 знаков. Если корней нет, выводится 'x ∈ ∅'.")
    print("Пример: solve_cubic 1 -2 1 0")
    print("Результат: 0 1 1")

def main():
    # Check number of arguments
    if len(sys.argv) != 5 and len(sys.argv) != 2:
        print("Ошибка: требуется 4 коэффициента или аргумент help.", file=sys.stderr)
        sys.exit(1)
        
    # Handle help
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        print_help()
        sys.exit(0)
    
    # Parse coefficients
    try:
        coeffs = [float(arg) for arg in sys.argv[1:]]
        a, b, c, d = coeffs
    except ValueError:
        print("Ошибка: все аргументы должны быть вещественными числами.", file=sys.stderr)
        sys.exit(1)
    
    # Solve equation
    roots = solve_cubic(a, b, c, d)
    
    # Handle infinite solutions
    if roots == [float('inf')]:
        print("x ∈ ℝ", file=sys.stdout)
        sys.exit(0)
        
    # Print roots
    if len(roots):
        formatted_roots = [f"{int(round(root))}" if abs(root - round(root)) < 1e-6 else f"{root:.3f}" for root in roots]
        print(" ".join(formatted_roots))
    else:
        print("x ∈ ∅")
    
        
if __name__ == "__main__":
    main()