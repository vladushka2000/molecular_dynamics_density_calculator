import dataclasses

from abstracts import particle


@dataclasses.dataclass
class LAMMPSParticle(particle.Particle):
    """
    Класс, описывающий свойства частицы ПО LAMMPS
    """

    particle_id: int
