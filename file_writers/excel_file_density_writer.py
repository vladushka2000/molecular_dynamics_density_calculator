import xlsxwriter

from abstracts import density, file_writer


class ExcelFileDensityWriter(file_writer.FileWriter):
    """
    Врайтер плотностей в excel-файл
    """

    def write_to_file(self, file_name: str, content: list[density.Density]) -> None:
        """
        Записать в excel-файл
        :param file_name: название файла для записи
        :param content: содержимое для записи
        """
        workbook = xlsxwriter.Workbook(f"{file_name}.xlsx")
        worksheet = workbook.add_worksheet()

        row = 0
        coord_column = 0
        value_column = 1

        worksheet.write(row, coord_column, "Координата x")
        worksheet.write(row, value_column, "Плотность")

        row += 1

        for item in content:
            worksheet.write(row, coord_column, item.coord)
            worksheet.write(row, value_column, item.value)

            row += 1

        workbook.close()
