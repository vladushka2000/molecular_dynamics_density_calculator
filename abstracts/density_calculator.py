import abc
import math
import os
import re
from typing import Optional

from abstracts import (
    density as abs_density,
    density_calculator_init_values as calculator_init_values,
    particle as abs_particle,
    system as abs_system,
)
from common import const
from dto import layer as dto_layer, md_file_content


class DensityCalculator(abc.ABC):
    """
    Абстрактный калькулятор плотностей, реализующий шаблонный метод
    """

    def __init__(
        self, init_values: calculator_init_values.CalculatorInitValues
    ) -> None:
        """
        Инициализировать переменные
        :param init_values: исходные значения дла расчета
        """
        self.init_values = init_values

    @abc.abstractmethod
    def get_files_by_file_name_mask(
        self, directory_path: str, file_name_mask: str
    ) -> list[str]:
        """
        Получить файлы, удовлетворяющие переданной маске названия файла
        :param directory_path: путь до файлов
        :param file_name_mask: маска имени файла
        :return: пути до файлов с результатами моделирования
        """

        def _is_file_name_valid(file_name: str, mask: str) -> bool:
            """
            Провалидировать имя файла
            :param file_name: название файла
            :param mask: маска для названия файла
            :return: True, если название и тип файла соответствуют требуемым, иначе False
            """
            return file_name.endswith(
                const.CalculatorConsts.LAMMPS_FILE_EXTENSION
            ) and re.findall(mask, file_name)

        dir_path = os.path.realpath(directory_path)
        roots = []

        for name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, name)

            if os.path.isfile(full_path) and _is_file_name_valid(name, file_name_mask):
                roots.append(full_path)

        return roots

    @abc.abstractmethod
    def parse_data_file(self, path: str) -> md_file_content.MDFileContent:
        """
        Распарсить файл с результатами моделирования
        :param path: путь до файла
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_particles_coords_from_parsed_file(
        self, file_content: md_file_content.MDFileContent, axis_adjustment: float
    ) -> list[abs_particle.Particle]:
        """
        Получить объекты частиц из содержимого файла с результатами моделирования
        :param file_content: содержимое файла
        :param axis_adjustment: значение для корректировки расчета координаты
        :return: список объектов частиц
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_system_properties_from_parsed_file(
        self, file_content: md_file_content.MDFileContent
    ) -> abs_system.System:
        """
        Получить свойства системы из содержимого файла с результатами моделирования
        :param file_content: содержимое файла
        :return: объект свойств системы
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_layers(
        self,
        particles: list[abs_particle.Particle],
        axis_length: float,
        layers_num: int,
    ) -> list[dto_layer.Layer]:
        """
        Создать объекты слоев системы
        :param particles: объекты частиц
        :param axis_length: длина системы
        :param layers_num: количество слоев
        :return: объекты слоев
        """
        layer_width = axis_length / layers_num
        layers = [
            dto_layer.Layer(layer_num=layer_num, coord=layer_width * layer_num)
            for layer_num in range(layers_num)
        ]

        for particle in particles:
            if particle.coord_x <= axis_length:
                layer_num = math.ceil(particle.coord_x / layer_width) - 1
                layer_particles_types = layers[layer_num].particle_types

                if particle.particle_type not in [
                    types.particle_type for types in layer_particles_types
                ]:
                    layers[layer_num].particle_types.append(
                        dto_layer.LayerParticleTypeProperties(
                            particle_type=particle.particle_type, particles_num=1
                        )
                    )
                else:
                    for particle_type in layer_particles_types:
                        if particle.particle_type == particle_type.particle_type:
                            particle_type.particles_num += 1

                            break

        return layers

    @abc.abstractmethod
    def get_densities(
        self,
        layers: list[dto_layer.Layer],
        layers_num: int,
        system_volume: float,
        mol_mass: float,
        particle_type_ids: Optional[list[int]] = None,
    ) -> list[abs_density.Density]:
        """
        Получить плотности системы по слоям
        :param layers: объекты слоев
        :param layers_num: количество слоев
        :param system_volume: объем системы
        :param mol_mass: молярная масса
        :param particle_type_ids: учитываемые типы частиц для расчета
        """
        densities = []

        for layer in layers:
            particles_num = 0

            if particle_type_ids is None:
                particles_num = sum(
                    [type_.particles_num for type_ in layer.particle_types]
                )
            else:
                for type_ in layer.particle_types:
                    if type_.particle_type in particle_type_ids:
                        particles_num += type_.particles_num

            densities.append(
                abs_density.Density(
                    coord=layer.coord,
                    layer_num=layer.layer_num,
                    value=(
                        particles_num
                        * mol_mass
                        * layers_num
                        * const.CalculatorConsts.ATOMIC_UNIT_OF_MASS_TO_KG
                        / (
                            system_volume
                            * const.CalculatorConsts.ANGSTROM_TO_M
                            * const.CalculatorConsts.ANGSTROM_TO_M
                            * const.CalculatorConsts.ANGSTROM_TO_M
                        )
                    ),
                )
            )

        return densities

    @abc.abstractmethod
    def calculate_mean_densities(
        self, densities_per_file: list[list[abs_density.Density]], layers_num: int
    ) -> list[abs_density.Density]:
        """
        Рассчитать средние значения плотностей из нескольких файлов
        :param densities_per_file: список плотностей, рассчитанных из файлов
        :param layers_num: количество слоев
        :return: список усредненных плотностей
        """
        mean_densities = []

        for layer_num in range(layers_num):
            densities_sum = 0

            for densities_set in densities_per_file:
                densities_sum += densities_set[layer_num].value

            mean_densities.append(
                abs_density.Density(
                    coord=densities_per_file[0][layer_num].coord,
                    layer_num=layer_num,
                    value=densities_sum / len(densities_per_file),
                )
            )

        return mean_densities

    @abc.abstractmethod
    def write_to_file(self, densities: list[abs_density.Density]) -> None:
        """
        Записать значения плотностей в файл
        :param densities: список рассчитанных плотностей
        """
        self.init_values.file_writer.write_to_file(
            self.init_values.result_file_name, densities
        )

    def calculate(self) -> None:
        """
        Рассчитать плотности и записать в файл
        """
        densities_per_file = []
        files_paths = self.get_files_by_file_name_mask(
            self.init_values.directory_path, self.init_values.file_name_mask
        )

        if not files_paths:
            raise ValueError("Файлы с результатами моделирования не были найдены")

        for file_path in files_paths:
            file_content = self.parse_data_file(file_path)
            system_properties = self.get_system_properties_from_parsed_file(
                file_content
            )
            particles = self.get_particles_coords_from_parsed_file(
                file_content, system_properties.length_x / 2
            )
            layers = self.create_layers(
                particles, system_properties.length_x, self.init_values.layers_num
            )
            system_volume = (
                system_properties.length_x
                * system_properties.length_y
                * system_properties.length_z
            )
            densities = self.get_densities(
                layers,
                self.init_values.layers_num,
                system_volume,
                self.init_values.mol_mass,
                self.init_values.particle_type_ids,
            )
            densities_per_file.append(densities)

        mean_densities = self.calculate_mean_densities(
            densities_per_file, self.init_values.layers_num
        )

        self.write_to_file(mean_densities)
