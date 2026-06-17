import sys
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from Core.dataverse_base import DataverseBase


class DataverseMultiSelectCreator(DataverseBase):

    def create_multiselect(self, table, schema, label, values):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"

        cleaned_values = [v for v in values if v and v.lower() != "nan"]
        options = []
        for i, v in enumerate(cleaned_values):
            options.append({
                "Value": 100000000 + i,
                "Label": self.label(v)
            })

        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.MultiSelectPicklistAttributeMetadata",
            "SchemaName": schema,
            "DisplayName": self.label(label),
            "OptionSet": {
                "@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata",
                "IsGlobal": False,
                "Options": options
            }
        }

        return self.call("POST", url, payload)

    def run(self):
        with open("schema/multiselects.json", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            table = item["table"]
            schema = item["schema_name"]

            if not schema.startswith("msp_"):
                print(f"skip standard {table}.{schema}")
                continue

            if not self.exists_table(table):
                print(f" skip {table}.{schema} (table absente)")
                continue

            if self.exists_attribute(table, schema):
                print(f"exists {table}.{schema}")
                continue

            print(f"create {table}.{schema}")
            self.create_multiselect(table, schema, item["label"], item["values"])
            self.wait(1)

        self.publish_all()
        print("DONE")


if __name__ == "__main__":
    DataverseMultiSelectCreator().run()