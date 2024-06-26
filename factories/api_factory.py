from abstracts import api, factory
from api import cli
from common import enums


class APIFactory(factory.Factory):
    """
    Фабрика объектов API
    """

    def __init__(self, api_type: enums.APIType = enums.APIType.CLI) -> None:
        """
        Инициализировать переменные
        """
        self.api_type = api_type

    def create_instance(self) -> api.API:
        """
        Создать объект API
        :return: объект API
        """
        match self.api_type:
            case enums.APIType.CLI.value:
                return cli.CLI()
            case _:
                raise ValueError("Передан неверный тип API")
