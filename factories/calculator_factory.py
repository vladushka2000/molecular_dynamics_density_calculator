from abstracts import (
    density_calculator,
    density_calculator_init_values as calculator_init_values,
    factory,
)
from calculators import lammps_density_calculator
from common import enums


class CalculatorFactory(factory.Factory):
    """
    Фабрика объектов калькулятора
    """

    def create_instance(
        self,
        init_values: calculator_init_values.CalculatorInitValues,
        calculator_type: enums.MDProgram,
    ) -> density_calculator.DensityCalculator:
        """
        Создать объект калькулятора
        :param init_values: объект исходных значений для калькулятора
        :param calculator_type: тип калькулятора
        :return: объект калькулятора
        """
        match calculator_type:
            case enums.MDProgram.LAMMPS:
                return lammps_density_calculator.LAMMPSDensityCalculator(init_values)
            case _:
                raise ValueError("Передан неверный тип калькулятора")
