import enum


class MDProgram(enum.Enum):
    """
    Enum названия программы для молекулярного моделирования
    """

    LAMMPS = "LAMMPS"


class APIType(enum.Enum):
    """
    Enum для типов API
    """

    CLI = "CLI"


class FileWriterType(enum.Enum):
    """
    Enum для типов врайтеров
    """

    EXCEL = "excel"
