from models import *
import streamlit as st
from utils import *
import pandas as pd
import time
from datetime import datetime, timedelta



######################################################################

def formulaire(coach_data, nom_classe=None):
    with st.form(key="formulaire"):
        valeurs = {}
        champs = list(coach_data.keys()) if isinstance(coach_data, dict) else coach_data

        for champ in champs:
            if champ.lower() in ["id", "coach_id", "id_carteacces"]:
                continue

            # Gestion spéciale pour Inscription
            if nom_classe == Inscription:
                if champ.lower() == "id_membre":
                    membres = afficher_membres()
                    membres_options = [{"id": m.id, "nom": f"{m.prenom} {m.nom}"} for m in membres]
                    membre_selectionne = st.selectbox("Sélectionnez un membre", options=membres_options, format_func=lambda x: x["nom"])
                    valeurs[champ] = membre_selectionne["id"]
                elif champ.lower() == "id_cours":
                    cours = afficher_cours()
                    cours_options = [{"id": c.id,"sport": c.sport,"horaire": c.horaire} for c in cours]
                    cours_selectionne = st.selectbox("Sélectionnez un cours", options=cours_options, format_func=lambda x: f"{x['sport']} - {x['horaire'].strftime('%d/%m/%Y %H:%M')}")
                    valeurs[champ] = cours_selectionne["id"]
                valeurs["date_inscription"] = datetime.now().date()
                continue  # Passe au champ suivant

            # Gestion des champs standards
            if champ.lower() == "genre":
                if isinstance(coach_data, dict):
                    index = 0 if coach_data[champ] == "Masculin" else 1
                index_genre = st.radio(champ, ["Masculin", "Feminin"], 
                    index=index if isinstance(coach_data, dict) else 0)
                valeurs[champ] = index_genre

            elif champ.lower() == "date_naissance":
                valeurs[champ] = st.date_input(champ, 
                    value=coach_data[champ] if isinstance(coach_data, dict) else None)

            elif champ.lower() == "coach":
                coachs = afficher_coachs()
                coach_selectionne = st.selectbox("Sélectionnez un coach", options=coachs, format_func=lambda x: x["nom"])
                valeurs["coach_id"] = coach_selectionne["id"]

            elif champ.lower() == "horaire":
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input(f"{champ} (date)", 
                        value=coach_data[champ].date() if isinstance(coach_data, dict) else None)
                with col2:
                    heure = st.time_input(f"{champ} (heure - de 9h à 16h (la salle ferme à 17h) )", 
                        value=coach_data[champ].time() if isinstance(coach_data, dict) else None, 
                        step=timedelta(hours=1))
                if date is not None and heure is not None:
                    valeurs[champ] = datetime.combine(date, heure)

            else:
                valeurs[champ] = st.text_input(champ, 
                    value=coach_data[champ] if isinstance(coach_data, dict) else None)

        col1, col2 = st.columns(2)
        with col1:
            mettre_a_jour = st.form_submit_button("Valider")
        with col2:
            annuler = st.form_submit_button("Annuler")

        if annuler:
            return "annuler"
        elif mettre_a_jour:
            if isinstance(coach_data, dict) and "id" in coach_data:  # Si c'est une modification
                identifiant = coach_data["id"]
                for champ, valeur in valeurs.items():
                    if champ != "id":  # ne pas modifier l'ID
                        resultat = modifier_donnee(nom_classe, identifiant, champ, valeur)
                        if not resultat:
                            st.error(f"Erreur lors de la modification du champ {champ}")
                            return None
                return valeurs
            else:  # Si c'est une création
                if nom_classe == Cours:  # Vérifications spéciales pour les cours
                    resultat = inserer_donnees(valeurs, nom_classe)
                    if resultat is not None:  # Si une erreur est retournée
                        st.warning(str(resultat))
                        return None
                return valeurs
    return None

######################################################################

def supprimer_entree(nom_classe, db_index) :
    if 'boutons_confirmation' not in st.session_state:
        st.session_state.boutons_confirmation = False
    if st.button("Supprimer", key="bouton_suprimer"):
        st.session_state.afficher_form = False
        st.session_state.afficher_form_modifier = False
        st.session_state.boutons_confirmation = True
    if st.session_state.boutons_confirmation:
        st.warning("Voulez-vous Confirmer la suppression?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Oui", key="confirm_yes"):
                supprimer_donnee(nom_classe, db_index)
                st.success("Suppression réussie.")
                time.sleep(2)
                st.session_state.boutons_confirmation = False
                st.rerun()
        with col2:
            if st.button("Non", key="confirm_no"):
                st.session_state.boutons_confirmation = False
                st.rerun()

######################################################################

if 'afficher_form' not in st.session_state:
    st.session_state.afficher_form = False
    
if 'afficher_form_modifier' not in st.session_state:
    st.session_state.afficher_form_modifier = False

def accueil() : 
    st.title("Interface administrateur")
    st.markdown("""
    L'interface administrateur offre une gestion complète des activités liées aux coachs et aux cours.

    **Les principales fonctionnalités incluent :**

    • La possibilité d'ajouter, de modifier ou de supprimer des coachs, garantissant ainsi une équipe dynamique et adaptée aux besoins des membres.

    • La gestion des cours, permettant aux administrateurs d'effectuer des modifications ou des suppressions selon les exigences.

    • La visualisation des membres inscrits à chaque cours, facilitant ainsi le suivi des participations.

    • La possibilité d'annuler une inscription ou un cours, assurant une flexibilité optimale dans la gestion des activités.
    """)    

######################################################################

def gestion(nom_classe, liste_champs) : 
    st.header(f"Gérer les {nom_classe.__str__()}")
    if nom_classe == Cours : 
        donnees_brutes = afficher_cours()
    elif nom_classe == Inscription : 
        donnees_brutes = afficher_inscriptions()
    else :
        donnees_brutes = selectionner_donnees(nom_classe)
    liste_donnees = []
    
    if not donnees_brutes:
        st.info(f"Aucune donnée disponible pour {nom_classe.__name__}")
        # Créer un DataFrame vide 
        df_donnees = pd.DataFrame(columns=liste_champs)
    else : 
        # Créer le DataFrame
        for donnee in donnees_brutes :
            dict_donnee = {champ: getattr(donnee, champ) for champ in liste_champs}
            liste_donnees.append(dict_donnee)
        df_donnees = pd.DataFrame(liste_donnees)   
        st.dataframe(df_donnees, hide_index=True, width=1200, height=300)    

    if nom_classe == Cours : 
        fonction_format = lambda x: f"{df_donnees.loc[x, 'sport']} {df_donnees.loc[x, 'horaire']}"
    elif nom_classe == Coach : 
        fonction_format = lambda x: f"{df_donnees.loc[x, 'prenom']} {df_donnees.loc[x, 'nom']}"
    elif nom_classe == Inscription : 
        fonction_format = lambda x: f"{df_donnees.loc[x, 'membre']} - {df_donnees.loc[x, 'cours']} - {df_donnees.loc[x, 'date_inscription']}"
    elif nom_classe == Membre : 
        fonction_format = lambda x: f"{df_donnees.loc[x, 'prenom']} {df_donnees.loc[x, 'nom']}  |  téléphone : {df_donnees.loc[x, 'telephone']}"
        
    if not donnees_brutes :
        if st.button("Ajouter", key="bouton_ajouter"):
            st.session_state.afficher_form = True
            st.session_state.afficher_form_modifier = False
        if st.session_state.afficher_form:
            nouvelles_donnees = formulaire(liste_champs,nom_classe)
            
            if nouvelles_donnees  == "annuler" :
                st.session_state.afficher_form = False
                st.rerun()
            elif nouvelles_donnees is not None :
                inserer_donnees(nouvelles_donnees, nom_classe)
                st.success(f"{nom_classe.__str__()} ajouté(e) avec succès")
                st.session_state.afficher_form = False
                time.sleep(2)
                st.rerun()

    elif donnees_brutes :
        index_selection_donnee = st.selectbox(f"Sélectionnez un(e) {nom_classe.__str__()} à supprimer :",df_donnees.index,format_func=fonction_format)
        
        db_index_donnee = int(df_donnees.loc[index_selection_donnee, 'id'])
        
        if db_index_donnee is not None and db_index_donnee is not None :
            col1, col2, col3 = st.columns(3)
        
        # bouton ajouter
            with col1 :
                if st.button("Ajouter", key="bouton_ajouter"):
                    st.session_state.afficher_form = True
                    st.session_state.afficher_form_modifier = False
            if st.session_state.afficher_form:
                nouvelles_donnees = formulaire(liste_champs,nom_classe)
                
                if nouvelles_donnees  == "annuler" :
                    st.session_state.afficher_form = False
                    st.rerun()
                elif nouvelles_donnees is not None :
                    inserer_donnees(nouvelles_donnees, nom_classe)
                    st.success(f"{nom_classe.__str__()} ajouté(e) avec succès")
                    st.session_state.afficher_form = False
                    time.sleep(2)
                    st.rerun()
                    
            # bouton de modification
            with col2:
                if st.button("Modifier", key="bouton_modifier"):
                    st.session_state.afficher_form_modifier = True
                    st.session_state.afficher_form_ajout = False

            if st.session_state.afficher_form_modifier:
                modif_data = df_donnees.loc[index_selection_donnee].to_dict()
                coach_modifs = formulaire(modif_data,nom_classe)
    
                if coach_modifs == "annuler" :
                    st.session_state.afficher_form_modifier = False
                    st.rerun()
                elif coach_modifs is not None:
                    for champ, nouvelle_valeur in coach_modifs.items():
                        if champ != 'id':  # On ne modifie pas l'id
                            modifier_donnee(nom_classe, db_index_donnee, champ, nouvelle_valeur)
                    st.success("Modification réussie")
                    time.sleep(2)
                    st.session_state.afficher_form_modifier = False
                    st.rerun()

            with col3:
                supprimer_entree(nom_classe, db_index_donnee)


##########################################################################################

choix = ("Accueil", "Gérer les coachs", "Gérer les cours", "Gérer les inscriptions", "Gérer Membres")
with st.sidebar : 
    add_radio = st.radio("Faites un choix : ", choix)

if add_radio == "Accueil" : 
    accueil()

elif add_radio == "Gérer les coachs" :
    liste_champs = ["id", "prenom", "nom", "sport", "genre", "date_naissance", "email", "telephone"]
    gestion(Coach, liste_champs)

elif add_radio == "Gérer les cours" : 
    liste_champs = ["id", "sport", "horaire", "capacite_max", "nombre_inscrits", "coach_id", "coach"]
    gestion(Cours, liste_champs)

elif add_radio == "Gérer les inscriptions" : 
    liste_champs = ["id", "id_membre", "membre","id_cours", "cours", "date_inscription"]
    gestion(Inscription, liste_champs)
    
elif add_radio == "Gérer Membres" : 
    liste_champs = ["id", "prenom", "nom", "genre", "date_naissance", "email", "telephone", "id_carteAcces"]
    gestion(Membre, liste_champs)