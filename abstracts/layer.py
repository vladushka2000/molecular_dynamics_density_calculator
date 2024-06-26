import dataclasses
from typing import Optional


@dataclasses.dataclass
class LayerParticleTypeProperties:
    """
    Класс, описывающий тип частиц и их количество
    """

    particle_type: int
    particles_num: int


@dataclasses.dataclass
class Layer:
    """
    Класс, описывающий слой системы
    """

    layer_num: int
    coord: float
    particle_types: Optional[list[LayerParticleTypeProperties]] = dataclasses.field(
        default_factory=lambda: []
    )
