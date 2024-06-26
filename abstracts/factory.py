import abc


class Factory(abc.ABC):
    """
    Абстрактный класс фабрики
    """

    @abc.abstractmethod
    def create_instance(self, *args, **kwargs) -> any:
        """
        Создать объект
        :return: создаваемый объект
        """
        raise NotImplementedError
