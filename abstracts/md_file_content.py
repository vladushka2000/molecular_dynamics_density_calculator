import dataclasses


@dataclasses.dataclass
class MDFileContent:
    """
    Класс, описывающий содержимое файлов с результатами моделирования
    """

    particles: list[str]
    system_properties: list[str]
