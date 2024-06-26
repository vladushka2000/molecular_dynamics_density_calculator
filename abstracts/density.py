import dataclasses


@dataclasses.dataclass
class Density:
    """
    Абстрактный класс, описывающий свойства плотности
    """

    coord: float
    layer_num: int
    value: float
