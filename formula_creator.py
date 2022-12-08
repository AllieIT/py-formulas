from __future__ import annotations

import sympy as sp
from typing import Dict, Tuple, List

from formula import Formula
from quantity import PhysicalQuantity


class FormulaCreator:
    """
    Wrapper class used to create formulas and perform physical calculations
    """

    __name: str
    __abbr: str
    __unit: str | None
    __quantities: Dict[sp.Symbol, PhysicalQuantity]
    __formula: Formula | None

    def __init__(self, name: str, abbr: str, unit: str = None):
        """
        Args:
            name (str): Full name of quantity
            abbr (str): Short name for quantity
        """
        self.__name = name
        self.__abbr = abbr
        self.__unit = unit

        self.__quantities = {}
        self.__formula = None

    def create_quantity(self, name: str, abbr: str):
        """
        Create a new quantity and return symbol for use in formula

        Args:
            name (str): Full name of quantity
            abbr (str): Short name for quantity

        Returns:
            SymPy symbol used for creating formulas
        """
        p = PhysicalQuantity(name, abbr)
        self.__quantities[p.symbol] = p
        return p.symbol

    def set_formula(self, formula: sp.Expr):
        """
        Create a formula from SymPy expression

        Args:
            formula (sp.Expr): Formula
        """
        self.__formula = Formula(
            self.__name,
            self.__abbr,
            self.__unit if self.__unit else "",
            formula,
            *[self.__quantities[symbol] for symbol in formula.atoms(sp.Symbol)]
        )

    def set_unit(self, unit: str):
        """
        Set unit for a result

        Args:
            unit (str): String representation uf unit, e.g. m/s^2
        """
        self.__unit = unit

    def set_values_and_uncertainties(self, values: Dict[sp.Symbol, Tuple[float | List[float], float]],
                                     type_a: bool = False):
        """
        Sets values and uncertainties for each of specified quantities
        Args:
            values (Dict[sp.Symbol, Tuple[float | List[float], float]]): Dictionary of symbols and their respective
            tuples matching pattern (values, uncertainty), where uncertainty is of type B
            type_a (bool): Specifies if type A uncertainty should be calculated, argument used only for list of values
        """

        for key, item in values.items():
            quantity = self.__quantities[key]
            if isinstance(item[0], list):
                quantity.set_values_from_list(item[0], item[1], type_a=type_a)
            else:
                quantity.set_value_and_uncertainty(*item)

    def set_print_options(self, digits: int):
        self.__formula.set_print_options(digits)

    def calculate(self):
        return self.__formula.calculate()