import dataclasses

from abstracts import md_file_content


@dataclasses.dataclass
class MDFileContent(md_file_content.MDFileContent):
    """
    Класс, описывающий содержимое файлов с результатами моделирования
    """

    pass
