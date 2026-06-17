import pandas as pd


class SheetParser:
    TYPE_HINTS = [
        "Texte", "Texte long", "Texte (URL)", "Texte (email)", "Texte (téléphone)",
        "Recherche", "Rechercher",
        "Liste de valeurs", "Liste de valeur",
        "Liste de valeurs sélection multiple", "Selected items",
        "Booléen", "Date", "Date et heure",
        "Nombre entier", "Nombre %", "Nombre décimal", "Devise"
    ]

    def _norm(self, value):
        return str(value).strip().lower().replace("é", "e").replace("è", "e")

    def _is_type(self, value):
        v = self._norm(value)
        return any(self._norm(h) in v for h in self.TYPE_HINTS)

    def find_header_row(self, df):
        for idx, row in df.iterrows():
            values = [self._norm(v) for v in row.tolist() if pd.notna(v)]
            if any("nom champ" in v for v in values) and any("nom logique" in v for v in values):
                return idx
        return -1

    def _find_col_index(self, header_values, needle):
        for i, v in enumerate(header_values):
            if needle in self._norm(v):
                return i
        return -1

    def parse_rows(self, df):
        header_row = self.find_header_row(df)

        if header_row == -1:
            print("  Header non trouvé")
            return []

        header_values = [str(v).strip() if pd.notna(v) else "" for v in df.iloc[header_row].tolist()]

        idx_label = self._find_col_index(header_values, "nom champ")
        idx_logical = self._find_col_index(header_values, "nom logique")
        idx_type = self._find_col_index(header_values, "type")
        idx_values = self._find_col_index(header_values, "valeur")

        if idx_label == -1 or idx_logical == -1 or idx_type == -1:
            print("  Colonnes obligatoires non trouvées")
            return []

        records = []
        current = None

        work = df.iloc[header_row + 1:]

        for _, row in work.iterrows():
            vals = row.tolist()

            label = str(vals[idx_label]).strip() if idx_label < len(vals) and pd.notna(vals[idx_label]) else ""
            logical = str(vals[idx_logical]).strip() if idx_logical < len(vals) and pd.notna(vals[idx_logical]) else ""
            source_type = str(vals[idx_type]).strip() if idx_type < len(vals) and pd.notna(vals[idx_type]) else ""
            value_cell = str(vals[idx_values]).strip() if idx_values != -1 and idx_values < len(vals) and pd.notna(vals[idx_values]) else ""

            # ligne vide
            if not label and not logical and not source_type and not value_cell:
                continue

            # nouveau champ : on a au moins un "logical" ou un vrai type
            if logical or self._is_type(source_type):
                if current:
                    records.append(current)

                current = {
                    "label": label or "",
                    "logical_name": logical or "",
                    "source_type": source_type or "",
                    "values": []
                }

                if value_cell:
                    current["values"].append(value_cell)
                continue

            # sinon : continuation des valeurs d'une picklist / multiselect
            if current:
                # récupère toutes les cellules non vides de la ligne comme valeurs supplémentaires
                extra = [str(v).strip() for v in vals if pd.notna(v) and str(v).strip()]
                if extra:
                    current["values"].extend(extra)

        if current:
            records.append(current)

        return records