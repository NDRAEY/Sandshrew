def trapezoidal_rule(f, a, b, sub=100):
    h = (b - a) / sub
    sum = 0.5 * (f(a) + f(b))
    for i in range(1, sub):
        x = a + i * h
        sum += f(x)
    return h * sum
