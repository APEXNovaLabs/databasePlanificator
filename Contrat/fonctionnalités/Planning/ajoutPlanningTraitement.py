import aiomysql
import asyncio
from datetime import datetime, timedelta

async def get_db_credentials():
    """Demande à l'utilisateur les identifiants de connexion à la base de données."""
    print("\nVeuillez entrer les informations de connexion à la base de données MySQL:")
    host = input("Entrez l'adresse du serveur MySQL (par défaut, localhost): ").strip()
    if not host:
        host = "localhost"

    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ").strip()
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306

    user = input("Entrez le nom d'utilisateur MySQL: ").strip()
    password = input("Entrez le mot de passe MySQL: ").strip()
    database = input("Entrez le nom de la base de données MySQL (par défaut, Planificator): ").strip()
    if not database:
        database = "Planificator"
    return host, port, user, password, database

async def get_public_holidays(pool, year: int) -> set[datetime.date]:
    """
    Récupère les dates des jours fériés pour une année donnée depuis la base de données.
    Nécessite une table `JoursFeries` avec une colonne `date_ferie` de type DATE.
    """
    public_holidays = set()
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Assuming you have a table named JoursFeries with a column date_ferie
                await cur.execute("SELECT date_ferie FROM JoursFeries WHERE YEAR(date_ferie) = %s", (year,))
                results = await cur.fetchall()
                for row in results:
                    if 'date_ferie' in row and isinstance(row['date_ferie'], datetime):
                        public_holidays.add(row['date_ferie'].date())
                    elif 'date_ferie' in row and isinstance(row['date_ferie'], datetime.date):
                        public_holidays.add(row['date_ferie'])
    except Exception as e:
        print(f"**Avertissement:** Erreur lors de la récupération des jours fériés: {e}. Les jours fériés ne seront pas pris en compte.")
    return public_holidays

def is_holiday_or_sunday(date_to_check: datetime.date, public_holidays: set[datetime.date]) -> bool:
    """
    Vérifie si une date donnée est un dimanche ou un jour férié.
    """
    # date.weekday() returns 6 for Sunday
    if date_to_check.weekday() == 6:
        return True
    if date_to_check in public_holidays:
        return True
    return False

async def ajouter_planning_traitement(pool, traitement_id: int, redondance_value: int, redondance_unit: str, date_debut_planification: datetime.date):
    """
    Ajoute un planning pour un traitement donné en générant des détails de planification.
    Prend en compte les jours fériés et les dimanches.
    """
    conn = None
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Vérifier si le traitement existe
                await cur.execute("SELECT traitement_id FROM Traitement WHERE traitement_id = %s", (traitement_id,))
                traitement_exists = await cur.fetchone()

                if not traitement_exists:
                    print(f"**Erreur:** Traitement avec l'ID {traitement_id} non trouvé. Opération annulée.")
                    return

                # Définir une date de fin (par exemple, 1 an à partir de la date de début)
                date_fin_planification = date_debut_planification + timedelta(days=365)
                print(f"Planification générée du {date_debut_planification} au {date_fin_planification}.")

                # Insérer le planning principal
                await cur.execute("""
                    INSERT INTO Planning (traitement_id, redondance, date_debut_planification, date_fin_planification)
                    VALUES (%s, %s, %s, %s)
                """, (traitement_id, f"{redondance_value} {redondance_unit}", date_debut_planification, date_fin_planification))

                planning_id = cur.lastrowid
                if not planning_id:
                    print("**Erreur:** Impossible d'obtenir le planning_id après insertion. Opération annulée.")
                    return

                print(f"Planning principal créé avec ID: {planning_id}")

                # Récupérer les jours fériés pour l'année en cours et l'année prochaine si la période s'étend sur deux ans
                public_holidays_current_year = await get_public_holidays(pool, date_debut_planification.year)
                public_holidays_next_year = await get_public_holidays(pool, date_fin_planification.year)
                all_public_holidays = public_holidays_current_year.union(public_holidays_next_year)


                # Calculer et insérer les détails de la planification
                current_date = date_debut_planification
                details_added_count = 0

                while current_date <= date_fin_planification:
                    # Ajuster la date si c'est un dimanche ou un jour férié
                    while is_holiday_or_sunday(current_date, all_public_holidays):
                        print(f"La date {current_date} est un dimanche ou un jour férié. Déplacement au jour suivant.")
                        current_date += timedelta(days=1)

                    # Insérer le détail de planification uniquement si la date est dans la période et validée
                    if current_date <= date_fin_planification:
                        await cur.execute("""
                            INSERT INTO PlanningDetails (planning_id, date_planification, statut, element_planification)
                            VALUES (%s, %s, 'À venir', 'Traitement')
                        """, (planning_id, current_date))
                        details_added_count += 1
                    else:
                        # Si la date ajustée dépasse la date de fin, ne pas l'ajouter
                        break


                    # Calculer la prochaine date de planification
                    if redondance_unit == 'jours':
                        current_date += timedelta(days=redondance_value)
                    elif redondance_unit == 'semaines':
                        current_date += timedelta(weeks=redondance_value)
                    elif redondance_unit == 'mois':
                        try:
                            new_month = current_date.month + redondance_value
                            new_year = current_date.year + (new_month - 1) // 12
                            new_month = (new_month - 1) % 12 + 1
                            current_date = current_date.replace(year=new_year, month=new_month)
                        except ValueError:
                            current_date = (current_date.replace(day=1) +
                                            timedelta(days=32 * redondance_value)).replace(day=1) - timedelta(days=1)
                    elif redondance_unit == 'ans':
                        current_date = current_date.replace(year=current_date.year + redondance_value)
                    else:
                        print(f"**Avertissement:** Unité de redondance '{redondance_unit}' non valide. Arrêt de la planification.")
                        break

                print(f"{details_added_count} détails de planification ajoutés pour le traitement {traitement_id}.")

    except Exception as e:
        print(f"**Erreur lors de l'ajout du planning :** {e}")

async def main():
    pool = None
    try:
        # Get DB credentials
        host, port, user, password, database = await get_db_credentials()

        # Create connection pool
        print(f"\nTentative de connexion à la base de données '{database}' sur {host}:{port} avec l'utilisateur '{user}'...")
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True,
            minsize=1,
            maxsize=5
        )
        print("Connexion à la base de données établie avec succès.")

        while True:
            print("\n--- Ajout d'un nouveau planning de traitement ---")
            traitement_id_input = input("Entrez l'ID du traitement (laissez vide pour quitter) : ").strip()
            if not traitement_id_input:
                break

            try:
                traitement_id = int(traitement_id_input)
            except ValueError:
                print("**Erreur :** L'ID du traitement doit être un nombre entier.")
                continue

            redondance_value_input = input("Entrez la valeur de la redondance (ex: 1 pour chaque mois, 2 pour chaque 2 semaines) : ").strip()
            if not redondance_value_input:
                break
            try:
                redondance_value = int(redondance_value_input)
                if redondance_value <= 0:
                    print("**Erreur :** La valeur de redondance doit être un nombre positif.")
                    continue
            except ValueError:
                print("**Erreur :** La valeur de redondance doit être un nombre entier.")
                continue

            redondance_unit_input = input("Entrez l'unité de la redondance (jours, semaines, mois, ans) : ").strip().lower()
            if redondance_unit_input not in ['jours', 'semaines', 'mois', 'ans']:
                print("**Erreur :** Unité de redondance non valide. Veuillez choisir parmi 'jours', 'semaines', 'mois', 'ans'.")
                continue

            date_debut_planification_str = input("Date de début de la planification (YYYY-MM-DD) : ").strip()
            if not date_debut_planification_str:
                break
            try:
                date_debut_planification = datetime.strptime(date_debut_planification_str, '%Y-%m-%d').date()
            except ValueError:
                print("**Erreur :** Format de date invalide. Utilisez le format YYYY-MM-DD.")
                continue

            await ajouter_planning_traitement(pool, traitement_id, redondance_value, redondance_unit_input, date_debut_planification)

            continuer = input("Voulez-vous ajouter un autre planning ? (oui/non) : ").strip().lower()
            if continuer != 'oui':
                break

    except Exception as e:
        print(f"**Une erreur inattendue est survenue dans le script principal :** {e}")
    finally:
        if pool:
            print("\nFermeture du pool de connexions à la base de données...")
            pool.close()
            await pool.wait_closed()
            print("Pool de connexions fermé.")

if __name__ == "__main__":
    asyncio.run(main())