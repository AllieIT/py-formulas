from __future__ import annotations

import numpy as np
import sympy as sp
from typing import Dict, List

from numpy.typing import ArrayLike

from print_options import PrintOptions
from uncertainties import Uncertainties


class PhysicalQuantity:

    name: str
    abbr: str
    symbol: sp.Symbol
    uncertainty: float | None
    value: float | None
    uncertainty_symbol: sp.Symbol | None
    print_options: PrintOptions

    __legal_options: List[str] = ["type_a"]

    def __init__(self, name: str, abbr: str):
        self.name = name
        self.abbr = abbr
        self.symbol = sp.Symbol(abbr)
        self.uncertainty = None
        self.uncertainty_symbol = sp.Symbol(f"u({self.symbol.name})")
        self.print_options = PrintOptions()

    def set_uncertainty(self, uncertainty: float):
        self.uncertainty = uncertainty

    def set_value(self, value: float):
        self.value = value

    def set_value_and_uncertainty(self, value: float, uncertainty: float):
        self.value = value
        self.uncertainty = uncertainty

    def set_values_from_list(self, values: ArrayLike, type_b: float = 0, **options: bool):
        for item in options:
            if item not in self.__legal_options:
                raise KeyError(f"Invalid keyword argument {item}")

        mean = np.average(values)
        type_a = 0
        if "type_a" in options:
            _, type_a = Uncertainties.get_type_a(values)

        total_uncertainty = (type_a ** 2 + type_b ** 2) ** 0.5

        print(
            "-------------------------------------\n" +
            f"Value set:".ljust(20) + f"{round(mean, self.print_options.digits)}\n" +
            f"Type A uncertainty:".ljust(20) + f"{round(type_a, self.print_options.digits) if type_a != 0 else '-'}\n" +
            f"Type B uncertainty:".ljust(20) + f"{round(type_b, self.print_options.digits) if type_b != 0 else '-'}\n" +
            f"Total uncertainty:".ljust(20) + f"{round(total_uncertainty, self.print_options.digits) if total_uncertainty != 0 else '-'}\n" +
            "-------------------------------------"
        )

    def set_print_options(self, digits: int = 16) -> None:
        self.print_options.digits = digits

    def get_sp_symbol(self):
        return self.symbol

    def get_subs(self):
        return [
            (self.symbol, self.value),
            (self.uncertainty_symbol, self.uncertainty)
        ]

