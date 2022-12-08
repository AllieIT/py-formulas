import numpy as np
from numpy.typing import ArrayLike


class Uncertainties:

    @staticmethod
    def get_type_a(values: ArrayLike):
        try:
            n = values.shape[0]
        except AttributeError:
            values = np.array(values)
            n = values.shape[0]
        mean = np.average(values)
        stddev = np.sqrt(1 / (n - 1) * np.sum((values - mean) ** 2))

        return mean, stddev
