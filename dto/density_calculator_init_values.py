import dataclasses
from abstracts import density_calculator_init_values as init_values


@dataclasses.dataclass
class CalculatorInitValues(init_values.CalculatorInitValues):
    """
    Модель исходных данных для расчета плотностей
    """

    pass
