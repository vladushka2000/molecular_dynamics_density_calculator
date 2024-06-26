from abstracts import factory, file_writer
from calculators import lammps_density_calculator
from common import enums
from file_writers import excel_file_density_writer


class FileWriterFactory(factory.Factory):
    """
    Фабрика объектов врайтеров
    """

    def create_instance(
        self,
        writer_type: enums.FileWriterType,
    ) -> file_writer.FileWriter:
        """
        Создать объект врайтера
        :param writer_type: тип врайтера
        :return: объект калькулятора
        """
        match writer_type:
            case enums.FileWriterType.EXCEL:
                return excel_file_density_writer.ExcelFileDensityWriter()
            case _:
                raise ValueError("Передан неверный тип врайтера")
