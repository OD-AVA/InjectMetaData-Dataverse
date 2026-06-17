import sys
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from Core.dataverse_base import DataverseBase


class DataverseTablesCreator(DataverseBase):

    def create_table(self, t):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions"

        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
            "SchemaName": t["table_schema"],
            "DisplayName": self.label(t["display"]),
            "DisplayCollectionName": self.label(t["plural"]),
            "OwnershipType": "UserOwned",
            "IsActivity": False,
            "HasActivities": False,
            "HasNotes": False,
            "PrimaryNameAttribute": t["primary_attr"],
            "Attributes": [{
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "SchemaName": t["primary_attr"],
                "DisplayName": self.label(t.get("primary_display", "Name")),
                "RequiredLevel": {"Value": "ApplicationRequired"},
                "MaxLength": 200,
                "FormatName": {"Value": "Text"},
                "IsPrimaryName": True
            }]
        }

        return self.call("POST", url, payload)

    def run(self):
        with open("schema/tables.json", encoding="utf-8") as f:
            tables = json.load(f)

        for t in tables:
            
            if self.exists_table(t["table_schema"]):
                print(f"[INFO] Table déjà existante : {t['table_schema']}")

                print("[AI] Vérification de la solution Dataverse...")

                print(
                    f"[IMPORTANT] La table doit être incluse dans la solution '{self.solution}' "
                    "pour permettre l'ajout des champs et des composants."
                )

                print(
                    "[NOTE] Les règles de gestion et conventions sont décrites dans le README du projet."
                )

                continue

            print(f"create {t['table_schema']}")
            self.create_table(t)
            self.wait(2)

        self.publish_all()


if __name__ == "__main__":
    DataverseTablesCreator().run()