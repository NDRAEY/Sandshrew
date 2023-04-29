from math import sin

def derivate(fn, x, h = .000000001):
    return (fn(x + h) - fn(x - h)) / (2 * h)

