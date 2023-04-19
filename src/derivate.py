def derivate(fn, x, h = .00000000001):
    return (fn(x + h) - fn(x - h)) / (2 * h)
