import math
import numpy as np

# Wavelengths of light

l_s = np.array([4047, 4078, 4358, 5460, 5770, 5791], dtype=float)
l_s = l_s * 10 ** -10

# Diffraction grating slit spacing
d = 2 * 10 ** -6

for n in range(4):
    print(f"n = {n}")
    for l in l_s:
        if n * l / d <= 1:
            a = 360 - math.asin(n * l / d) * 180 / math.pi
            floor = math.floor(a)
            a = (floor, round((a - floor) * 60))
            print(f"| Expected angle for length {round(l * 10 ** 10) / 10} nm: {a[0]}°{a[1]}'")
        else:
            print(f"| Can't calculate angle for length {round(l * 10 ** 10) / 10} nm")


