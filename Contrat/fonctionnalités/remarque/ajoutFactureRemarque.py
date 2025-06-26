import aiomysql
import asyncio
from datetime import datetime

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

async def ajouter_facture_remarque(pool, remarque_id: int):
    """
    Crée une facture automatique pour une remarque si le traitement associé est "Effectué"
    et si la remarque n'est pas déjà liée à une facture "Payée".
    """
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                print(f"Tentative de création de facture pour la remarque ID: {remarque_id}...")

                # 1. Récupérer les informations de la remarque et vérifier son statut et sa facture associée
                # On veut une remarque dont le PlanningDetails est 'Effectué'
                # ET soit elle n'a pas de facture associée (r.facture_id IS NULL),
                # SOIT sa facture associée n'est PAS encore 'Payé' (pour gérer un cas de re-facturation si besoin).
                await cur.execute("""
                    SELECT
                        r.remarque_id,
                        r.planning_detail_id,
                        pd.statut AS planning_detail_statut,
                        f.etat AS facture_etat,
                        f.facture_id AS existing_facture_id
                    FROM Remarque r
                    JOIN PlanningDetails pd ON r.planning_detail_id = pd.planning_detail_id
                    LEFT JOIN Facture f ON r.facture_id = f.facture_id
                    WHERE r.remarque_id = %s
                """, (remarque_id,))
                remarque_info = await cur.fetchone()

                if not remarque_info:
                    print(f"**Erreur:** Remarque avec l'ID {remarque_id} non trouvée.")
                    return

                planning_detail_id = remarque_info['planning_detail_id']
                planning_detail_statut = remarque_info['planning_detail_statut']
                facture_etat = remarque_info['facture_etat']
                existing_facture_id = remarque_info['existing_facture_id']

                if planning_detail_statut != 'Effectué':
                    print(f"**Action requise:** Le statut du PlanningDetails ({planning_detail_statut}) pour la remarque {remarque_id} n'est pas 'Effectué'. La facture ne peut pas être créée.")
                    return

                if existing_facture_id and facture_etat == 'Payé':
                    print(f"**Information:** La remarque {remarque_id} est déjà associée à une facture (ID: {existing_facture_id}) qui est 'Payé'. Aucune nouvelle facture ne sera créée.")
                    return
                elif existing_facture_id and facture_etat != 'Payé':
                    print(f"**Information:** La remarque {remarque_id} est déjà associée à une facture (ID: {existing_facture_id}) qui est '{facture_etat}'. La facture existante sera mise à jour ou une nouvelle sera créée si vous choisissez de continuer.")
                    # Vous pourriez ajouter ici une logique pour demander à l'utilisateur s'il veut mettre à jour l'ancienne facture
                    # ou créer une nouvelle. Pour l'instant, nous créerons une nouvelle par simplicité.

                # 2. Récupérer les informations nécessaires pour la facture (axe, date_planification)
                await cur.execute("""
                    SELECT
                        c.axe,
                        pd.date_planification
                    FROM Contrat c
                    JOIN Traitement t ON c.contrat_id = t.contrat_id
                    JOIN Planning p ON t.traitement_id = p.traitement_id
                    JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                    WHERE pd.planning_detail_id = %s
                """, (planning_detail_id,))
                facture_details_from_planning = await cur.fetchone()

                if not facture_details_from_planning:
                    print(f"**Erreur:** Informations de contrat/planning non trouvées pour planning_detail_id {planning_detail_id}. Impossible de créer la facture.")
                    return

                axe = facture_details_from_planning['axe']
                date_traitement = facture_details_from_planning['date_planification']

                # 3. Calculer le montant de la facture (exemple : 100, car Facture.montant est INT)
                # ATTENTION: Si vos montants peuvent avoir des décimales, Facture.montant devrait être DECIMAL(10,2)
                montant = 100

                # 4. Ajouter la nouvelle facture
                await cur.execute("""
                    INSERT INTO Facture (planning_detail_id, montant, date_traitement, axe, etat)
                    VALUES (%s, %s, %s, %s, 'À venir') -- Nouvelle facture est initialement 'À venir'
                """, (planning_detail_id, montant, date_traitement, axe)) # 'Payé' retiré de l'insertion, 'À venir' par défaut

                new_facture_id = cur.lastrowid
                if not new_facture_id:
                    print("**Erreur:** Impossible d'obtenir l'ID de la nouvelle facture après insertion.")
                    return

                print(f"Facture ID {new_facture_id} ajoutée avec succès pour PlanningDetails ID {planning_detail_id}.")

                # 5. Mettre à jour la remarque avec le nouveau facture_id
                await cur.execute("""
                    UPDATE Remarque SET facture_id = %s WHERE remarque_id = %s
                """, (new_facture_id, remarque_id))
                print(f"Remarque ID {remarque_id} mise à jour avec facture_id {new_facture_id}.")

                # conn.commit() # Redondant si autocommit=True sur le pool
                print("Opération terminée.")

    except Exception as e:
        print(f"**Une erreur est survenue lors de l'ajout de la facture/remarque :** {e}")

async def main():
    pool = None
    try:
        host, port, user, password, database = await get_db_credentials()

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
            print("\n--- Ajout d'une facture automatique pour une remarque ---")
            remarque_id_input = input("Entrez l'ID de la remarque (laissez vide pour quitter) : ").strip()
            if not remarque_id_input:
                break

            try:
                remarque_id = int(remarque_id_input)
            except ValueError:
                print("**Erreur :** L'ID de la remarque doit être un nombre entier.")
                continue

            await ajouter_facture_remarque(pool, remarque_id)

            continuer = input("\nVoulez-vous traiter une autre remarque ? (oui/non) : ").strip().lower()
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