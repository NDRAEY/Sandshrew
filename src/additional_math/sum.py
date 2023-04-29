def math_sum(start, stop, fn):
    a = 0

    for i in range(start, stop + 1):
        a += fn(i)

    return a
