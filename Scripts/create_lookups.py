import sys
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from Core.dataverse_base import DataverseBase


class DataverseRelationshipsCreator(DataverseBase):

    def create_relationship(self, table, field, target, label):
        url = f"{self.url}/api/data/v9.2/RelationshipDefinitions"

        payload = {
            "@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata",
            "SchemaName": f"{table}_{field}_{target}",
            "ReferencedEntity": target,
            "ReferencingEntity": table,
            "Lookup": {
                "@odata.type": "Microsoft.Dynamics.CRM.LookupAttributeMetadata",
                "SchemaName": field,
                "DisplayName": self.label(label)
            }
        }

        return self.call("POST", url, payload)

    def run(self):
        print("=== CREATE LOOKUPS FROM JSON ===")

        with open("schema/lookups.json", encoding="utf-8") as f:
            lookups = json.load(f)

        for l in lookups:
            table = l["table"]
            field = l["schema_name"]
            target = l.get("target_table")
            label = l["label"]

            if not field:
                print(f"[SKIP] lookup sans schema_name sur {table}")
                continue

            # on skip les champs standards
            if not field.startswith("msp_"):
                print(f"[SKIP] standard {table}.{field}")
                continue

            if not target:
                print(f"[SKIP] {table}.{field} (target_table manquant)")
                continue

            if not self.exists_table(table):
                print(f"[SKIP] {table}.{field} (table absente)")
                continue

            if self.exists_attribute(table, field):
                print(f"[SKIP] exists {table}.{field}")
                continue

            print(f"create {table}.{field} -> {target}")
            self.create_relationship(table, field, target, label)
            self.wait(2)

        self.publish_all()
        print("DONE")


if __name__ == "__main__":
    DataverseRelationshipsCreator().run()
