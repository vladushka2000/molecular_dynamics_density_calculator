import dataclasses


@dataclasses.dataclass
class Particle:
    """
    Абстрактный класс, описывающий свойства частицы
    """

    coord_x: float
    coord_y: float
    coord_z: float

    particle_type: int
