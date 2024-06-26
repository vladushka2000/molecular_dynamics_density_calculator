import dataclasses

from abstracts import file_writer


@dataclasses.dataclass
class CalculatorInitValues:
    """
    Модель исходных данных для расчета плотностей
    """

    directory_path: str
    file_name_mask: str
    layers_num: int
    mol_mass: float
    result_file_name: str
    particle_type_ids: list[int] | None
    file_writer: file_writer.FileWriter
