import openpyxl

def extract_formulas_to_markdown(excel_path, markdown_path):
    wb = openpyxl.load_workbook(excel_path, data_only=False)
    md_lines = [
        "# Extraction des formules Excel\n",
        "Ce document liste les formules trouvées dans le fichier Excel, organisées par feuille et par colonne.\n",
        "**Exemple de rendu :**\n",
        "\n",
        "## Feuille : Feuille1\n",
        "| Colonne | Cellule | Formule | Valeur calculée |\n",
        "|---------|---------|---------|-----------------|\n",
        "| Débit   | B2      | =A2*2   | 10              |\n",
        "\n",
        "---\n"
    ]

    for sheet in wb.sheetnames:
        ws = wb[sheet]
        md_lines.append(f"\n## Feuille : {sheet}\n")
        md_lines.append("| Colonne | Cellule | Formule | Valeur calculée |")
        md_lines.append("|---------|---------|---------|-----------------|")
        found = False
        # On suppose que la première ligne contient les en-têtes
        headers = {}
        for col in ws.iter_cols(1, ws.max_column, 1, 1):
            cell = col[0]
            if cell.value:
                headers[cell.column] = str(cell.value)
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                if cell.data_type == 'f' or (cell.value and isinstance(cell.value, str) and cell.value.startswith('=')):
                    found = True
                    cell_address = cell.coordinate
                    formula = cell.value
                    # Valeur calculée (data_only=True donne la valeur, mais ici on veut la formule ET la valeur)
                    value = ws.parent[sheet][cell_address].value
                    # Nom de colonne depuis l'en-tête
                    col_name = headers.get(cell.column, f"Col {cell.column}")
                    md_lines.append(f"| {col_name} | {cell_address} | `{formula}` | {value} |")
        if not found:
            md_lines.append("_Aucune formule trouvée sur cette feuille._")

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(md_lines))

if __name__ == "__main__":
    extract_formulas_to_markdown("Reseaux_2.xlsx", "formules_extraites.md")