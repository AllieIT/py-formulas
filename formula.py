from __future__ import annotations

import sympy as sp
from typing import List
from dataclasses import dataclass

from print_options import PrintOptions
from quantity import PhysicalQuantity


class Results:

    formula_name: str
    unit: str
    value: float | None
    uncertainty: float | None

    def __init__(self, value: float, uncertainty: float, formula_name: str, unit: str):
        self.value = value
        self.uncertainty = uncertainty
        self.formula_name = formula_name
        self.unit = unit

    def __str__(self):
        return (
            "-------------------------------------\n" +
            f"Formula for {self.formula_name}:\n" +
            f"Result:".ljust(20) + f"{self.value} {self.unit}\n" +
            f"Uncertainty:".ljust(20) + f"{self.uncertainty} {self.unit}\n" +
            "-------------------------------------"
        )

    def unpack(self) -> List[float]:
        return [self.value, self.uncertainty]


class Formula:

    name: str
    abbr: str
    unit: str
    formula: sp.Expr
    quantities: List[PhysicalQuantity]
    print_options: PrintOptions

    def __init__(self, name: str, abbr: str, unit: str, formula: sp.Expr, *quantities: PhysicalQuantity):
        self.name = name
        self.abbr = abbr
        self.unit = unit
        self.formula = formula
        self.quantities = list(quantities)
        self.print_options = PrintOptions()

    def gauss_uncertainty_formula(self) -> sp.Expr:
        full_formula: sp.Expr = sp.sympify(0)
        for quantity in self.quantities:
            q_diff = self.formula.diff(quantity.symbol)
            value = (q_diff * quantity.uncertainty_symbol) ** 2
            full_formula += value
        full_formula = full_formula ** 0.5
        return full_formula

    def calculate_value(self) -> float:
        if any(quantity.value is None for quantity in self.quantities):
            raise Exception("Quantity numerical values are not set within objects.")
        subs = [quantity.get_subs()[0] for quantity in self.quantities]
        return self.formula.subs(subs)

    def calculate_uncertainty(self) -> float:
        if any(quantity.uncertainty is None or quantity.value is None for quantity in self.quantities):
            raise Exception("Uncertainty or quantity numerical values are not set within objects.")
        subs = []
        for quantity in self.quantities:
            subs.extend(quantity.get_subs())
        return self.gauss_uncertainty_formula().subs(subs)

    def calculate(self) -> Results:
        return Results(
            round(self.calculate_value(), self.print_options.digits),
            round(self.calculate_uncertainty(), self.print_options.digits),
            self.name,
            self.unit
        ) if self.print_options.digits != 0 else Results(
            round(self.calculate_value()),
            round(self.calculate_uncertainty()),
            self.name,
            self.unit
        )

    def set_print_options(self, digits: int = 16) -> None:
        self.print_options.digits = digits