import wrapper

if __name__=="__main__":
    code = '''
    deg2rad(deg) = deg * pi / 180

    sin_my(deg) = {
        rads = deg2rad(deg)

        sin_tailor(x) = (-1) ^ x * ((rads ^ (2x + 1)) / (2x + 1)!)

        return sum(0, 25, sin_tailor)
    }

    print(sin_my(60))
    '''

    tot = wrapper.run_code(code)

    print(tot)
