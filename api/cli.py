import argparse

from abstracts import api, density_calculator
from common import const, enums, types
from dto import api_user_input, density_calculator_init_values as init_values
from factories import file_writer_factory


class CLI(api.API):
    """
    Класс cli для работы с программой
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """
        self.cmd_parser = argparse.ArgumentParser(
            description="Расчет плотностей в каждом слое для системы, состоящей из n типов частиц."
        )

    def get_user_input(self) -> api_user_input.APIUserInput:
        """
        Получить введенные пользоваталем данные
        :return: объект исходных данных для расчета
        """
        self.cmd_parser.add_argument(
            "path",
            type=types.DirPathType(),
            help="Путь к директории с файлами результатов моделирования",
        )
        self.cmd_parser.add_argument(
            "file_name_mask",
            type=str,
            help=(
                "Маска для названий файлов с результатами моделирования. "
                "Пример: 'result_file_' для набора из файлов с названиями 'result_file_1', 'result_file_2', ..."
            ),
        )
        self.cmd_parser.add_argument(
            "mol_mass", type=float, help="Молярная масса вещества, а.е.м."
        )
        self.cmd_parser.add_argument(
            "-p",
            "--program",
            type=enums.MDProgram,
            default=enums.MDProgram.LAMMPS,
            help="Название программы, в которой производилось моделирование. По-умолчанию: LAMMPS",
        )
        self.cmd_parser.add_argument(
            "-pt",
            "--particle-type",
            type=int,
            default=0,
            help="Тип исследуемой группы частиц в системе (для смесей). По-умолчанию: все типы частиц",
        )
        self.cmd_parser.add_argument(
            "-ln",
            "--layers-num",
            type=int,
            default=const.CalculatorConsts.DEFAULT_LAYERS_NUM,
            help="Количество слоев, на которые делится система для расчета плотностей. По-умолчанию: 100",
        )
        self.cmd_parser.add_argument(
            "-rw",
            "--result-writer",
            type=enums.FileWriterType,
            default=enums.FileWriterType.EXCEL,
            help="Тип итогового файла с рассчитанными плотностями",
        )
        self.cmd_parser.add_argument(
            "-rn",
            "--result-file-name",
            type=str,
            default="result",
            help="Название итогового файла с рассчитанными плотностями",
        )

        args = self.cmd_parser.parse_args()

        if args.particle_type == 0:
            args.particle_type = None

        writer = file_writer_factory.FileWriterFactory().create_instance(
            args.result_writer
        )

        calculator_init_values = init_values.CalculatorInitValues(
            directory_path=args.path,
            file_name_mask=args.file_name_mask,
            layers_num=args.layers_num,
            mol_mass=args.mol_mass,
            result_file_name=args.result_file_name,
            particle_type_ids=args.particle_type,
            file_writer=writer,
        )
        user_input = api_user_input.APIUserInput(
            calculator_init_values=calculator_init_values, program=args.program
        )

        return user_input

    def get_calculator(
        self,
        calculator_init_values: init_values.CalculatorInitValues,
        calculator_type: enums.MDProgram,
    ) -> density_calculator.DensityCalculator:
        return super().get_calculator(calculator_init_values, calculator_type)
