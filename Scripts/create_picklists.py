import sys
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from Core.dataverse_base import DataverseBase


class DataversePicklistCreator(DataverseBase):

    def create_picklist(self, table, schema, label, values):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"

        cleaned_values = [v for v in values if v and v.lower() != "nan"]
        options = []
        for i, v in enumerate(cleaned_values):
            options.append({
                "Value": 100000000 + i,
                "Label": self.label(v)
            })

        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.PicklistAttributeMetadata",
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
        with open("schema/picklists.json", encoding="utf-8") as f:
            picklists = json.load(f)

        for p in picklists:
            table = p["table"]
            schema = p["schema_name"]

            if not schema.startswith("msp_"):
                print(f" skip standard {table}.{schema}")
                continue

            if not self.exists_table(table):
                print(f" skip {table}.{schema} (table absente)")
                continue

            if self.exists_attribute(table, schema):
                print(f" exists {table}.{schema}")
                continue

            print(f"create {table}.{schema}")
            self.create_picklist(table, schema, p["label"], p["values"])
            self.wait(1)

        self.publish_all()
        print("DONE")


if __name__ == "__main__":
    DataversePicklistCreator().run()