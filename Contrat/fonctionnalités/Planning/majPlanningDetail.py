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

async def mettre_a_jour_planning_detail(pool, planning_detail_id: int, statut: str):
    """
    Met à jour le statut de PlanningDetails et enregistre l'historique si le statut est "Effectué".
    Affiche également les détails du planning avant la mise à jour.

    Args:
        pool: Le pool de connexions aiomysql.
        planning_detail_id (int): L'ID du détail de planification à mettre à jour.
        statut (str): Le nouveau statut ('Effectué' ou 'À venir').
    """
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 1. Récupérer et afficher les informations détaillées du planning_detail
                # Inclut le type de traitement, la redondance et le montant de la facture.
                await cur.execute("""
                    SELECT pd.planning_detail_id,
                           pd.planning_id,
                           pd.date_planification,
                           pd.statut,
                           tt.typeTraitement AS type_traitement,
                           p.redondance,
                           f.montant AS montant_facture,
                           f.facture_id,
                           f.etat AS etat_facture,
                           c.client_id,
                           CONCAT(cl.nom, ' ', cl.prenom) AS client_nom
                    FROM PlanningDetails pd
                    JOIN Planning p ON pd.planning_id = p.planning_id
                    JOIN Traitement t ON p.traitement_id = t.traitement_id
                    JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                    JOIN Contrat c ON t.contrat_id = c.contrat_id
                    JOIN Client cl ON c.client_id = cl.client_id
                    LEFT JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
                    WHERE pd.planning_detail_id = %s
                """, (planning_detail_id,))
                detail_info = await cur.fetchone()

                if not detail_info:
                    print(f"**Erreur:** Le détail de planification avec l'ID {planning_detail_id} n'existe pas. Aucune mise à jour effectuée.")
                    return

                print("\n--- Informations actuelles du détail de planification ---")
                print(f"ID Détail Planning: {detail_info['planning_detail_id']}")
                print(f"Client: {detail_info['client_nom']} (ID: {detail_info['client_id']})")
                print(f"Date de planification: {detail_info['date_planification'].strftime('%Y-%m-%d')}")
                print(f"Statut actuel: {detail_info['statut']}")
                print(f"Type de traitement: {detail_info['type_traitement']}")
                print(f"Redondance: {detail_info['redondance']} (1=mensuel, 2=bimensuel, 3=trimestriel, 4=quadrimestriel, 6=semestriel, 12=annuel)")
                print(f"Montant Facture: {detail_info['montant_facture']} Ar" if detail_info['montant_facture'] is not None else "Montant Facture: N/A")
                print(f"État Facture: {detail_info['etat_facture']}" if detail_info['etat_facture'] is not None else "État Facture: N/A")
                print("-----------------------------------------------------")

                # 2. Mettre à jour le statut de PlanningDetails
                await cur.execute("UPDATE PlanningDetails SET statut = %s WHERE planning_detail_id = %s", (statut, planning_detail_id))
                rows_affected = cur.rowcount

                if rows_affected == 0:
                    print(f"**Avertissement:** Aucune ligne mise à jour pour planning_detail_id {planning_detail_id}. Le statut était peut-être déjà '{statut}'.")
                else:
                    print(f"Statut du détail de planification {planning_detail_id} mis à jour en '{statut}'.")

                # 3. Enregistrer l'historique si le statut est "Effectué"
                if statut == "Effectué":
                    # Récupérer facture_id et définir des valeurs par défaut pour issue et action
                    facture_id_for_history = detail_info['facture_id']
                    issue_for_history = "Aucun problème signalé." # Valeur par défaut pour la colonne NOT NULL
                    action_for_history = "Traitement standard effectué." # Valeur par défaut pour la colonne NOT NULL

                    contenu_historique = f"Traitement effectué. Ancien statut: {detail_info['statut']}, Nouveau statut: {statut}. État de la facture: {detail_info['etat_facture'] if detail_info['etat_facture'] is not None else 'N/A'}."

                    # Assurez-vous que les colonnes 'issue' et 'action' sont fournies car elles sont NOT NULL
                    await cur.execute("""
                        INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, date_historique, contenu, issue, action)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (facture_id_for_history, planning_detail_id, None, datetime.now(), contenu_historique, issue_for_history, action_for_history))
                    print(f"Historique enregistré pour planning_detail_id {planning_detail_id}.")

    except Exception as e:
        print(f"**Erreur lors de la mise à jour du planning_detail {planning_detail_id}:** {e}")

async def main():
    pool = None # Initialiser le pool à None
    try:
        # Récupérer les identifiants de la base de données
        host, port, user, password, database = await get_db_credentials()

        # Créer le pool de connexions avec les identifiants fournis par l'utilisateur
        print(f"\nTentative de connexion à la base de données '{database}' sur {host}:{port} avec l'utilisateur '{user}'...")
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True, # Auto-commit les opérations
            minsize=1,       # Taille minimale du pool
            maxsize=5        # Taille maximale du pool
        )
        print("Connexion à la base de données établie avec succès.")

        while True:
            print("\n--- Mise à jour du statut d'un détail de planification ---")
            planning_detail_id_input = input("Entrez l'ID du détail de planification à mettre à jour (laissez vide pour quitter) : ").strip()
            if not planning_detail_id_input:
                break # Quitter la boucle si l'utilisateur n'entre rien

            try:
                planning_detail_id = int(planning_detail_id_input)
            except ValueError:
                print("**Erreur :** L'ID du détail de planification doit être un nombre entier. Veuillez réessayer.")
                continue # Recommencer la boucle

            statut_input = input("Entrez le nouveau statut ('Effectué' ou 'À venir') : ").strip()
            if statut_input.lower() not in ['effectué', 'à venir']:
                print("**Erreur :** Statut invalide. Veuillez entrer 'Effectué' ou 'À venir'.")
                continue # Recommencer la boucle

            # Capitaliser la première lettre pour correspondre aux valeurs de l'ENUM si nécessaire
            statut = statut_input.capitalize()

            await mettre_a_jour_planning_detail(pool, planning_detail_id, statut)

            # Demander à l'utilisateur s'il souhaite continuer
            reponse = input("\nVoulez-vous mettre à jour un autre détail de planification ? (oui/non) : ").strip().lower()
            if reponse != 'oui':
                break # Quitter la boucle si la réponse n'est pas 'oui'

    except Exception as e:
        print(f"**Une erreur inattendue est survenue dans le script principal :** {e}")
    finally:
        # S'assurer que le pool est fermé même en cas d'erreur
        if pool:
            print("\nFermeture du pool de connexions à la base de données...")
            pool.close()
            await pool.wait_closed()
            print("Pool de connexions fermé.")

if __name__ == "__main__":
    asyncio.run(main())
