from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def generer_planifications(traitement_id, date_debut, date_fin, redondance):
    """
    Génère des planifications mensuelles ou hebdomadaires pour un traitement donné.

    Args:
        traitement_id (int): L'identifiant du traitement.
        date_debut (date): La date de début de la planification.
        date_fin (date): La date de fin de la planification.
        redondance (str): La redondance de la planification ('Mensuel' ou 'Hebdomadaire').
    """

    date_courante = date_debut

    if redondance == "Mensuel":
        while date_courante <= date_fin:
            # Insérer dans la table PlanificationMensuelle
            inserer_planification_mensuelle(traitement_id, date_courante)
            date_courante = date_courante + relativedelta(months=1)  # Ajoute 1 mois

    elif redondance == "Hebdomadaire":
        while date_courante <= date_fin:
            # Insérer dans la table PlanificationHebdomadaire
            inserer_planification_hebdomadaire(traitement_id, date_courante)
            date_courante = date_courante + timedelta(weeks=1)  # Ajoute 1 semaine

def inserer_planification_mensuelle(traitement_id, date_planification):
    """
    Insère une planification mensuelle dans la base de données.

    Args:
        traitement_id (int): L'identifiant du traitement.
        date_planification (date): La date de la planification.
    """
    # + Insertion dans la DB
    print(f"Insertion dans PlanificationMensuelle: traitement_id={traitement_id}, date={date_planification}")

def inserer_planification_hebdomadaire(traitement_id, date_planification):
    """
    Insère une planification hebdomadaire dans la base de données.

    Args:
        traitement_id (int): L'identifiant du traitement.
        date_planification (date): La date de la planification.
    """
    # Insertion dans la DB
    print(f"Insertion dans PlanificationHebdomadaire: traitement_id={traitement_id}, date={date_planification}")
