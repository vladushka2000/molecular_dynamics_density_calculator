import dataclasses

from abstracts import layer


@dataclasses.dataclass
class LayerParticleTypeProperties(layer.LayerParticleTypeProperties):
    """
    Класс, описывающий тип частиц и их количество
    """

    pass


@dataclasses.dataclass
class Layer(layer.Layer):
    """
    Класс, описывающий слой системы
    """

    pass
