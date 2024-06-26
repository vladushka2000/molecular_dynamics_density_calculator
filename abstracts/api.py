import abc

from abstracts import (
    api_user_input,
    density_calculator,
    density_calculator_init_values as init_values,
)
from common import enums
from factories import calculator_factory


class API(abc.ABC):
    """
    Абстрактный класс API, реализующий шаблонный метод
    """

    @abc.abstractmethod
    def get_user_input(self) -> api_user_input.APIUserInput:
        """
        Получить введенные пользоваталем данные
        :return: объект исходных данных для расчета
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_calculator(
        self,
        calculator_init_values: init_values.CalculatorInitValues,
        calculator_type: enums.MDProgram,
    ) -> density_calculator.DensityCalculator:
        """
        Получить объект калькулятора по переданным пользователем данным
        :param calculator_init_values: объект исходных данных
        :param calculator_type: тип калькулятора
        :return: объект калькулятора
        """
        calculator = calculator_factory.CalculatorFactory().create_instance(
            calculator_init_values, calculator_type
        )

        return calculator

    def run(self) -> None:
        """
        Запустить приложение
        """
        user_input = self.get_user_input()
        calculator = self.get_calculator(
            user_input.calculator_init_values, user_input.program
        )

        calculator.calculate()
