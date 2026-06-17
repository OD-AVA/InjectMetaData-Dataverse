import json
from pathlib import Path


class SchemaDispatcher:

    def dispatch(self, tables):
        Path("schema").mkdir(exist_ok=True)

        tables_json = []
        fields = []
        picklists = []
        multiselects = []
        lookups = []

        for t in tables:

            # [OK] CREATE TABLES ONLY CUSTOM
            if t["is_custom"]:
                tables_json.append({
                    "table_schema": t["table_schema"],
                    "display": t["display"],
                    "plural": t["plural"],
                    "primary_attr": t["primary_attr"],
                    "primary_display": "Nom"
                })

            # [OK] FIELDS
            for f in t["fields"]:

                base = {
                    "table": f["table"],
                    "schema_name": f["schema_name"],
                    "label": f["label"],
                    "normalized_type": f["normalized_type"],
                    "values": f["values"]
                }

                if f["normalized_type"] in ("string", "boolean", "date", "datetime", "integer"):
                    fields.append(base)

                elif f["normalized_type"] == "picklist":
                    picklists.append(base)

                elif f["normalized_type"] == "multiselect":
                    multiselects.append(base)

                elif f["normalized_type"] == "lookup":
                    base["target_table"] = f.get("target_table")
                    lookups.append(base)

        self._write("tables.json", tables_json)
        self._write("fields.json", fields)
        self._write("picklists.json", picklists)
        self._write("multiselects.json", multiselects)
        self._write("lookups.json", lookups)

    def _write(self, name, data):
        with open(f"schema/{name}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)