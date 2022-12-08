import math
from typing import Tuple

import sympy

from formula_creator import FormulaCreator

# 1. Define functions


def convert_to_radians(angle_tuple: Tuple[int, int]) -> float:
    return math.radians(angle_tuple[0] + angle_tuple[1] / 60)


def convert_to_tuple(angle_deg: float) -> Tuple[int, int]:
    deg = math.degrees(angle_deg)
    return int(math.floor(deg)), int((deg - math.floor(deg)) * 60)


# 2. Set data

d = 2 * 10 ** -6
labels = ["Fiolet", "Niebieski", "Zielony", "Żółty I", "Żółty II"]

a_1 = {
    1: [(348, 19), (348, 14), (347, 25)],   # ...
    2: [(336, 8), ],  # ...
    3: [(322, 37), ],  # ...
}

a_2 = {
    1: [(11, 40), (11, 46), (12, 35)],  # ...
    2: [(23, 52), ],  # ...
    3: [(37, 23), ],  # ...
}

# 3. Preprocess data - transform dictionaries:

transform_angle = lambda x, y: (360 - x, y) if y == 0 else (359 - x, 60 - y)
mean_tuple = lambda x, y: convert_to_tuple(convert_to_radians(((x[0] + y[0]) / 2, (x[1] + y[1]) / 2)))

a_1 = {key: [transform_angle(*t) for t in a_1[key]] for key in a_1}
a_mean = {key: [mean_tuple(x_1, x_2) for x_1, x_2 in zip(a_1[key], a_2[key])] for key in a_1}

# 4. Create formula

f = FormulaCreator("Wavelength", "l", "A")

a = f.create_quantity("Angle", "a")
n = f.create_quantity("Series", "n")

formula = sympy.sin(a) * d / n * 10 ** 10
f.set_formula(formula)
f.set_print_options(digits=0)

# 5. Calculate

for i, angles in a_mean.items():
    print(f"n = {i}")
    angle_labels = labels[:len(angles)]
    for angle, label in zip(angles, angle_labels):
        f.set_values_and_uncertainties({
            a: (convert_to_radians(angle), math.radians(1 / 60)),
            n: (i, 0)
        })
        wavelength = f.calculate()
        print(label)
        print(wavelength)
        print("")
    print("")
