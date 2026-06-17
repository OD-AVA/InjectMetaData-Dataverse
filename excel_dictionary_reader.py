import pandas as pd


class ExcelDictionaryReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_all_sheets(self):
        xls = pd.ExcelFile(self.file_path)
        return {
            sheet: pd.read_excel(self.file_path, sheet_name=sheet, header=None)
            for sheet in xls.sheet_names
        }
