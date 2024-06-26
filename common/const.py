import dataclasses


class CLITypesConsts:
    """
    Константы для типов аргументов в CLI
    """

    FILE_NAME_DELIMETER = "_"
    FILE_NAME_END_RE_PATTERN = rf"file{FILE_NAME_DELIMETER}\d+"


class CalculatorConsts:
    """
    Константы для калькулятор плотностей
    """

    @dataclasses.dataclass
    class FileStartEndLine:
        """
        Модель начала и конца строк в файлах результатов моделирования
        """

        start_line: int
        end_line: int = dataclasses.field(default=None)

    LAMMPS_FILE_EXTENSION = ".data"
    LAMMPS_FILE_COORDS_LINES = FileStartEndLine(21)
    LAMMPS_FILE_SYSTEM_PROPERTIES_LINES = FileStartEndLine(5, 7)
    ATOMIC_UNIT_OF_MASS_TO_KG = 1.66 * 10 ** (-27)
    ANGSTROM_TO_M = 10 ** (-10)
    DEFAULT_LAYERS_NUM = 100
