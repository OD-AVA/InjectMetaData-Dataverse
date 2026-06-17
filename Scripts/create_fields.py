import sys
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from Core.dataverse_base import DataverseBase


class DataverseFieldsCreator(DataverseBase):

    def create_string(self, table, schema, label):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"
        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": schema,
            "DisplayName": self.label(label),
            "MaxLength": 200,
            "FormatName": {"Value": "Text"}
        }
        return self.call("POST", url, payload)

    def create_boolean(self, table, schema, label):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"
        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
            "SchemaName": schema,
            "DisplayName": self.label(label),
            "OptionSet": {
                "TrueOption": {
                    "Value": 1,
                    "Label": self.label("Yes")
                },
                "FalseOption": {
                    "Value": 0,
                    "Label": self.label("No")
                }
            }
        }
        return self.call("POST", url, payload)

    def create_integer(self, table, schema, label):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"
        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
            "SchemaName": schema,
            "DisplayName": self.label(label)
        }
        return self.call("POST", url, payload)

    def create_date(self, table, schema, label):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"
        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
            "SchemaName": schema,
            "DisplayName": self.label(label),
            "Format": "DateOnly"
        }
        return self.call("POST", url, payload)

    def run(self):
        print("=== CREATE FIELDS FROM JSON ===")

        with open("schema/fields.json", encoding="utf-8") as f:
            fields = json.load(f)

        for f_ in fields:
            table = f_["table"]
            schema = f_["schema_name"]
            label = f_["label"]
            field_type = f_["normalized_type"]

            if not schema:
                print(f"[SKIP] champ sans schema_name sur {table}")
                continue

            # skip standard
            if not schema.startswith("msp_"):
                print(f"[SKIP] standard {table}.{schema}")
                continue

            # skip si la table n'existe pas
            if not self.exists_table(table):
                print(f"[SKIP] {table}.{schema} (table absente)")
                continue

            # skip si le champ existe déjà
            if self.exists_attribute(table, schema):
                print(f"[SKIP] exists {table}.{schema}")
                continue

            print(f"create {table}.{schema}")

            if field_type == "string":
                self.create_string(table, schema, label)
            elif field_type == "boolean":
                self.create_boolean(table, schema, label)
            elif field_type == "integer":
                self.create_integer(table, schema, label)
            elif field_type in ("date", "datetime"):
                self.create_date(table, schema, label)
            else:
                print(f"[SKIP] type non géré {field_type} pour {table}.{schema}")

            self.wait(1)

        self.publish_all()
        print("DONE")


if __name__ == "__main__":
    DataverseFieldsCreator().run()
