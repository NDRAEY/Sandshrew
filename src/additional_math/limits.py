def limit(f, x, h=1e-6):
    return (f(x + h) - f(x)) / h
