

from excel_dictionary_reader import ExcelDictionaryReader
from sheet_parser import SheetParser
from schema_normalizer import SchemaNormalizer


class SchemaBuilder:

    def __init__(self, file):
        self.reader = ExcelDictionaryReader(file)
        self.parser = SheetParser()
        self.norm = SchemaNormalizer()

    def build(self):
        sheets = self.reader.load_all_sheets()
        tables = []

        for name, df in sheets.items():

            # [OK] TABLE
            table_info = self.norm.normalize_table(name)

            # [OK] PARSE
            rows = self.parser.parse_rows(df)

            table = {
                "table_schema": table_info["schema"],
                "display": table_info["display"],
                "plural": table_info["plural"],
                "primary_attr": f"{table_info['schema']}_name",
                "is_custom": table_info["is_custom"],
                "fields": []
            }

            for r in rows:

                field_name = self.norm.normalize_field_name(r["logical_name"])

                # [OK] skip si pas un vrai champ
                if not field_name:
                    continue

                field_type = self.norm.normalize_type(r["source_type"])

                field = {
                    "table": table_info["schema"],
                    "schema_name": field_name,
                    "label": r["label"] or field_name,
                    "normalized_type": field_type,
                    "values": r["values"]
                }

                table["fields"].append(field)

            tables.append(table)

        return tables
