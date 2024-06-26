import dataclasses

from abstracts import density_calculator_init_values as init_values
from common import enums


@dataclasses.dataclass
class APIUserInput:
    """
    Абстрактный класс, описывающий поля API, заполняемые пользователем
    """

    program: enums.MDProgram
    calculator_init_values: init_values.CalculatorInitValues
