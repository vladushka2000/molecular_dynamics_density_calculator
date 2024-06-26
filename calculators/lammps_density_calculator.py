from typing import Optional

from abstracts import density_calculator, file_writer
from common import const
from dto import density, layer, md_file_content, particle, system


class LAMMPSDensityCalculator(density_calculator.DensityCalculator):
    """
    Калькулятор плотностей, совместимый с ПО LAMMPS
    """

    def get_files_by_file_name_mask(
        self, directory_path: str, file_name_mask: str
    ) -> list[str]:
        """
        Рассчитать плотности системы по слоям
        :param directory_path: путь до файлов
        :param file_name_mask: маска имени файла
        :return: пути до файлов с результатами моделирования
        """

        return super().get_files_by_file_name_mask(directory_path, file_name_mask)

    def parse_data_file(
        self, path: str, *args, **kwargs
    ) -> md_file_content.MDFileContent:
        """
        Распарсить файл с результатами моделирования
        :param path: путь до файла
        """
        axes_rows = []
        particle_coords = []
        line_num = -1

        with open(path) as file:
            for line in file:
                line_num += 1

                if line_num in range(
                    const.CalculatorConsts.LAMMPS_FILE_SYSTEM_PROPERTIES_LINES.start_line,
                    const.CalculatorConsts.LAMMPS_FILE_SYSTEM_PROPERTIES_LINES.end_line
                    + 1,
                ):
                    axes_rows.append(line)

                if (
                    line_num
                    >= const.CalculatorConsts.LAMMPS_FILE_COORDS_LINES.start_line
                    and line != "\n"
                ):
                    particle_coords.append(line)
                elif (
                    line_num
                    >= const.CalculatorConsts.LAMMPS_FILE_COORDS_LINES.start_line
                    and line == "\n"
                ):
                    break

        file_content = md_file_content.MDFileContent(particle_coords, axes_rows)

        return file_content

    def get_particles_coords_from_parsed_file(
        self, file_content: md_file_content.MDFileContent, axis_adjustment: float
    ) -> list[particle.LAMMPSParticle]:
        """
        Получить объекты частиц из содержимого файла с результатами моделирования
        :param file_content: содержимое файла
        :param axis_adjustment: значение для корректировки расчета координаты
        :return: список объектов частиц
        """
        particles = []

        for line in file_content.particles:
            particle_peroperties = line.split()
            particles.append(
                particle.LAMMPSParticle(
                    particle_id=int(particle_peroperties[0]),
                    particle_type=int(particle_peroperties[1]),
                    coord_x=float(particle_peroperties[2]) + axis_adjustment,
                    coord_y=float(particle_peroperties[3]),
                    coord_z=float(particle_peroperties[4]),
                )
            )

        return particles

    def get_system_properties_from_parsed_file(
        self, file_content: md_file_content.MDFileContent
    ) -> system.LAMMPSSystem:
        """
        Получить свойства системы из содержимого файла с результатами моделирования
        :param file_content: содержимое файла
        :return: объект свойств системы
        """
        system_axes = []

        for row in file_content.system_properties:
            lengths = row.split()
            system_axes.append(abs(float(lengths[0])) + abs(float(lengths[1])))

        system_x_axis = system_axes[0]
        system_y_axis = system_axes[1]
        system_z_axis = system_axes[2]

        return system.LAMMPSSystem(
            length_x=system_x_axis, length_y=system_y_axis, length_z=system_z_axis
        )

    def create_layers(
        self,
        particles: list[particle.LAMMPSParticle],
        axis_length: float,
        layers_num: int,
    ) -> list[layer.Layer]:
        """
        Создать объекты слоев системы
        :param particles: объекты частиц
        :param axis_length: длина системы
        :param layers_num: количество слоев
        :return: объекты слоев
        """
        return super().create_layers(particles, axis_length, layers_num)

    def get_densities(
        self,
        layers: list[layer.Layer],
        layers_num: int,
        system_volume: float,
        mol_mass: float,
        particle_type_ids: Optional[list[int]] = None,
    ) -> list[density.Density]:
        """
        Получить плотности системы по слоям
        :param layers: объекты слоев
        :param layers_num: количество слоев
        :param system_volume: объем системы
        :param mol_mass: молярная масса
        :param particle_type_ids: учитываемые типы частиц для расчета
        """
        return super().get_densities(
            layers, layers_num, system_volume, mol_mass, particle_type_ids
        )

    def calculate_mean_densities(
        self, densities_per_file: list[list[density.Density]], layers_num: int
    ) -> list[density.Density]:
        """
        Рассчитать средние значения плотностей из нескольких файлов
        :param densities_per_file: список плотностей, рассчитанных из файлов
        :param layers_num: количество слоев
        :return: список усредненных плотностей
        """
        return super().calculate_mean_densities(densities_per_file, layers_num)

    def write_to_file(self, densities: list[density.Density]) -> None:
        """
        Записать значения плотностей в файл
        :param densities: список рассчитанных плотностей
        """
        super().write_to_file(densities)
