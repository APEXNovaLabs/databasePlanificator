# generate_traitements_report.py

import pandas as pd
import datetime
import asyncio
import aiomysql
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from connexionDB import DBConnection

# Connection à la base de données
DBConnection()
# --- Fonction de récupération des traitements pour un mois donné ---
async def get_traitements_for_month(year: int, month: int):
    conn = None
    try:
        conn = await aiomysql.connect(**DBConnection())
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT pd.date_planification        AS `Date du traitement`, \
                           tt.typeTraitement            AS `Traitement concerné`, \
                           tt.categorieTraitement       AS `Catégorie du traitement`, \
                           CONCAT(c.nom, ' ', c.prenom) AS `Client concerné`, \
                           c.categorie                  AS `Catégorie du client`, \
                           c.axe                        AS `Axe du client`
                    FROM PlanningDetails pd \
                             JOIN \
                         Planning p ON pd.planning_id = p.planning_id \
                             JOIN \
                         Traitement t ON p.traitement_id = t.traitement_id \
                             JOIN \
                         TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement \
                             JOIN \
                         Contrat co ON t.contrat_id = co.contrat_id \
                             JOIN \
                         Client c ON co.client_id = c.client_id
                    WHERE YEAR(pd.date_planification) = %s \
                      AND MONTH(pd.date_planification) = %s
                    ORDER BY pd.date_planification; \
                    """
            await cursor.execute(query, (year, month))
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération des traitements : {e}")
        return []
    finally:
        if conn:
            conn.close()


# --- Fonction pour générer le fichier Excel des traitements ---
def generate_traitements_excel(data: list[dict], year: int, month: int):
    month_name_fr = datetime.date(year, month, 1).strftime('%B').capitalize()
    file_name = f"traitements-{month_name_fr}-{year}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = f"Traitements {month_name_fr} {year}"

    # Styles
    bold_font = Font(bold=True)
    header_font = Font(bold=True, size=14)
    center_align = Alignment(horizontal='center', vertical='center')

    # Titre du rapport
    ws.cell(row=1, column=1, value=f"Rapport des Traitements du mois de {month_name_fr} {year}").font = header_font
    ws.cell(row=1, column=1).alignment = center_align
    # Merge cells for title (assuming 6 data columns for the report)
    num_data_cols = 6
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_data_cols)

    # Nombre total de traitements
    total_traitements = len(data)
    ws.cell(row=3, column=1, value=f"Nombre total de traitements ce mois-ci : {total_traitements}").font = bold_font

    # Ligne vide pour la séparation
    ws.cell(row=4, column=1, value="")

    # Initialiser df ici, même si 'data' est vide
    df = pd.DataFrame(data)

    if df.empty:  # Utiliser df.empty pour vérifier si des données ont été chargées
        ws.cell(row=5, column=1, value="Aucun traitement trouvé pour ce mois.")
    else:
        # Écrire les en-têtes de colonne
        headers = df.columns.tolist()
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_idx, value=header)
            cell.font = bold_font

        # Écrire les données
        for r_idx, row_data in enumerate(df.values.tolist(), start=6):
            for c_idx, value in enumerate(row_data, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)

    # Ajuster la largeur des colonnes
    # df est toujours défini ici, donc pas d'UnboundLocalError
    max_col_for_width = len(df.columns) if not df.empty else num_data_cols

    for i in range(1, max_col_for_width + 1):
        column_letter = get_column_letter(i)
        length = 0
        for row_idx in range(1, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=i)
            if cell.value is not None:
                length = max(length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = length + 2

    try:
        output = BytesIO()
        wb.save(output)
        with open(file_name, 'wb') as f:
            f.write(output.getvalue())

        print(f"Fichier '{file_name}' généré avec succès.")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier Excel des traitements : {e}")


# --- Fonction principale pour exécuter le rapport des traitements ---
async def main_traitements_report():
    while True:
        try:
            year_input = input("Veuillez entrer l'année pour le rapport des traitements (ex: 2023) : ")
            month_input = input(
                "Veuillez entrer le numéro du mois (1-12) pour le rapport des traitements (ex: 6 pour Juin) : ")

            selected_year = int(year_input)
            selected_month = int(month_input)

            if not (1 <= selected_month <= 12):
                print("Numéro de mois invalide. Veuillez entrer un nombre entre 1 et 12.")
                continue

            if not (2000 <= selected_year <= datetime.datetime.now().year + 1):
                print(f"Année invalide. Veuillez entrer une année entre 2000 et {datetime.datetime.now().year + 1}.")
                continue

            break
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre pour l'année et le mois.")

    print(
        f"\nPréparation du rapport des traitements pour {datetime.date(selected_year, selected_month, 1).strftime('%B').capitalize()} {selected_year}...")
    traitements_data = await get_traitements_for_month(selected_year, selected_month)
    generate_traitements_excel(traitements_data, selected_year, selected_month)


if __name__ == "__main__":
    asyncio.run(main_traitements_report())