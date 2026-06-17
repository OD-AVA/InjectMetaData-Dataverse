class SchemaNormalizer:

    STANDARD_TABLES = {
        "account": "account",
        "contact": "contact",
        "lead": "lead",
        "opportunity": "opportunity",
        "product": "product",
        "email": "email",
        "task": "task",
    }

    # [OK] CORRECT VERSION (IMPORTANT)
    def normalize_table(self, sheet_name):
        key = sheet_name.strip().lower()

        # standard tables
        if key in self.STANDARD_TABLES:
            schema = self.STANDARD_TABLES[key]
            is_custom = False

        else:
            # [OK] FIX DOUBLE MSP
            if key.startswith("msp_"):
                schema = key
            elif key.startswith("psm_") or key.startswith("spm_"):
                schema = "msp_" + key.split("_", 1)[1]
            else:
                schema = "msp_" + key

            is_custom = True

        display = self.clean_display(sheet_name)
        plural = display + "s"

        return {
            "schema": schema,
            "display": display,
            "plural": plural,
            "is_custom": is_custom
        }

    def clean_display(self, name):
        text = name.strip()
        for prefix in ["psm_", "spm_", "msp_"]:
            text = text.replace(prefix, "")
        return text.replace("_", " ").strip().title()

    def normalize_type(self, t):
        t = (t or "").lower().strip()

        if "recherche" in t:
            return "lookup"
        if "multi" in t or "selected" in t:
            return "multiselect"
        if "liste" in t:
            return "picklist"
        if "bool" in t:
            return "boolean"
        if "date et heure" in t:
            return "datetime"
        if "date" in t:
            return "date"
        if "nombre" in t:
            return "integer"

        return "string"

    def normalize_field_name(self, raw):
        if not raw:
            return None

        raw = raw.strip()

        # [OK] ignore les types mal parsés
        if raw.lower() in [
            "texte", "liste de valeurs", "recherche", "rechercher",
            "selected items", "booléen"
        ]:
            return None

        return raw