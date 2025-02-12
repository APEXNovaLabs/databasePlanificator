import bcrypt
import mysql.connector
from mysql.connector import Error

# Fonction pour établir une connexion à la base de données
def connect():
    while True:
        try:
            user = input("Nom d'utilisateur MySQL : ")
            password = input("Mot de passe MySQL : ")
            host = input("Hôte MySQL (laissez vide pour localhost) : ") or "localhost"
            database = input("Nom de la base de données : ")

            config = {
                'user': user,
                'password': password,
                'host': host,
                'database': database,
                'raise_on_warnings': True
            }

            conn = mysql.connector.connect(**config)
            print("Connexion à la base de données réussie !")
            return conn

        except Error as e:
            print(f"Erreur de connexion à la base de données : {e}")
            retry = input("Voulez-vous réessayer ? (oui/non) : ").lower()
            if retry != 'oui':
                return None

# Fonction pour vérifier si le mot de passe correspond aux informations personnelles
def password_is_personal_info(nom, prenom, password):
    return nom.lower() in password.lower() or prenom.lower() in password.lower()

# Fonction pour hacher le mot de passe avec bcrypt
def hash_password(password):
    # Générer un "salt" aléatoire
    salt = bcrypt.gensalt()
    # Hacher le mot de passe avec le salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Fonction pour demander un mot de passe valide (modifiée pour utiliser le hachage)
def get_valid_password(nom, prenom):
    while True:
        password = input("Entrez votre nouveau mot de passe : ")
        confirm_password = input("Confirmez votre nouveau mot de passe : ")

        if password != confirm_password:
            print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
        elif len(password) < 8:
            print("Le mot de passe doit contenir au moins 8 caractères.")
        elif password_is_personal_info(nom, prenom, password):
            print("Le mot de passe ne doit pas contenir votre nom ou prénom. Veuillez réessayer.")
        else:
            return hash_password(password)  # Hacher le mot de passe avant de le retourner

# Fonction pour créer un compte
def creation_compte(conn):
    nom = input("Entrez le nom : ")
    prenom = input("Entrez le prénom : ")
    email = input("Entrez l'email : ")
    type_compte = input("Entrez le type de compte (Administrateur/Utilisateur) : ")
    password = get_valid_password(nom, prenom)  # Le mot de passe est déjà haché

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Account (nom, prenom, email, password, type_compte)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nom, prenom, email, password, type_compte))
        conn.commit()
        print("Compte créé avec succès !")
    except Error as e:
        print(f"Erreur lors de la création du compte : {e}")

# Pour voir les comptes existants
def lecture_compte(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Account")
        accounts = cursor.fetchall()

        if accounts:  # Vérifier si la liste des comptes n'est pas vide
            print("\nListe des comptes :")
            for account in accounts:
                print(f"ID: {account[0]}, Nom: {account[1]}, Prénom: {account[2]}, Email: {account[3]}, Type: {account[5]}")
        else:
            print("\nAucun compte trouvé dans la base de données.")

    except Error as e:
        print(f"Erreur lors de la lecture des comptes : {e}")

# Fonction pour mettre à jour un compte
def update_compte(conn):
    account_id = input("Entrez l'ID du compte à mettre à jour : ")
    nom = input("Entrez le nouveau nom (laissez vide pour ne pas modifier) : ")
    prenom = input("Entrez le nouveau prénom (laissez vide pour ne pas modifier) : ")
    email = input("Entrez le nouvel email (laissez vide pour ne pas modifier) : ")
    password = input("Entrez le nouveau mot de passe (laissez vide pour ne pas modifier) : ")

    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if nom:
            updates.append("nom = %s")
            params.append(nom)
        if prenom:
            updates.append("prenom = %s")
            params.append(prenom)
        if email:
            updates.append("email = %s")
            params.append(email)
        if password:
            password = get_valid_password(nom if nom else "", prenom if prenom else "")
            updates.append("password = %s")
            params.append(password)

        if updates:
            query = f"UPDATE Account SET {', '.join(updates)} WHERE id = %s"
            params.append(account_id)
            cursor.execute(query, tuple(params))
            conn.commit()
            print("Compte mis à jour avec succès !")
        else:
            print("Aucune modification apportée.")
    except Error as e:
        print(f"Erreur lors de la mise à jour du compte : {e}")

def suppression_compte(conn):
    account_id = input("Entrez l'ID du compte à supprimer : ")
    admin_password = input("Entrez le mot de passe administrateur pour confirmer : ")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Account WHERE type_compte = 'Administrateur'")
        admin_db_password_hashed = cursor.fetchone()[0]

        # Convertir le mot de passe haché de la base de données en bytes
        admin_db_password_hashed_bytes = admin_db_password_hashed.encode('utf-8')

        if bcrypt.checkpw(admin_password.encode('utf-8'), admin_db_password_hashed_bytes):
            cursor.execute("DELETE FROM Account WHERE id = %s", (account_id,))
            conn.commit()
            print("Compte supprimé avec succès !")
        else:
            print("Mot de passe administrateur incorrect. Suppression annulée.")
    except Error as e:
        print(f"Erreur lors de la suppression du compte : {e}")

# Menu principal
def main():
    conn = connect()
    if not conn:
        return

    while True:
        print("\n--- Menu Principal ---")
        print("1. Créer un compte")
        print("2. Lister les comptes")
        print("3. Mettre à jour un compte")
        print("4. Supprimer un compte")
        print("5. Quitter")
        choice = input("Choisissez une option : ")

        if choice == '1':
            creation_compte(conn)
        elif choice == '2':
            lecture_compte(conn)
        elif choice == '3':
            update_compte(conn)
        elif choice == '4':
            suppression_compte(conn)
        elif choice == '5':
            break
        else:
            print("Option invalide. Veuillez réessayer.")

    conn.close()
    print("Déconnexion de la base de données.")

# Point d'entrée du script
if __name__ == "__main__":
    main()