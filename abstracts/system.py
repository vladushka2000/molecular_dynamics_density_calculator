import dataclasses


@dataclasses.dataclass
class System:
    """
    Абстрактный класс, описывающий свойства системы
    """

    length_x: float
    length_y: float
    length_z: float
