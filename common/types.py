import re
import os

from common import const


class DirPathType:
    """
    Тип переменной для пути к директории
    """

    def __call__(self, dir_string: str) -> str:
        """
        Проверить, является ли строка директорией
        :param dir_string: строка с директорией
        :return: строка с директорий
        """
        if os.path.isdir(dir_string):
            return dir_string

        raise NotADirectoryError(dir_string)


class FileNameType:
    """
    Тип маски для названия файлов с результатами моделирования
    """

    def __call__(self, dir_string: str) -> str:
        """
        Проверить, соответствует ли название файла маске
        :param dir_string: строка с названием файла
        :return: строка с названием файла
        """
        matches = re.findall(const.CLITypesConsts.FILE_NAME_END_RE_PATTERN, dir_string)

        if not matches or not dir_string.endswith(matches[0]):
            raise ValueError(dir_string)

        return dir_string
