import abc


class FileWriter(abc.ABC):
    """
    Абстрактный класс врайтера
    """

    @abc.abstractmethod
    def write_to_file(self, file_name: str, content: any) -> None:
        """
        Записать в файл
        :param file_name: название файла для записи
        :param content: содержимое для записи
        """
        raise NotImplementedError
