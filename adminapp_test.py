from models import *
import streamlit as st
from utils import *
import pandas as pd
import time


def nouveau_form(args) : 
    with st.form("nouveau_form"):
        valeurs = {}
        # champs = args
        for champ in args:
            if champ.lower() == "id":
                continue
            elif champ.lower() == "genre":
                index_genre = st.radio(champ, ["Masculin", "Feminin"])
                valeurs[champ] = "Masculin" if index_genre == "Masculin" else "Feminin"
            elif champ.lower() in ["date_naissance", "horaire"]:
                valeurs[champ] = st.date_input(champ)
            else:
                valeurs[champ] = st.text_input(champ)

        col1, col2 = st.columns(2)
        with col1:
            ajouter = st.form_submit_button("Ajouter")
        with col2:
            annuler = st.form_submit_button("Annuler")

        if annuler:
            return "annuler"
        elif ajouter:
            return valeurs
    return None


######################################################################

def modifier_form(coach_data):
    with st.form("modifier_form"):
        valeurs = {}
        # champs = [champ for champ in coach_data.keys()]
        for champ in coach_data.keys():
            if champ.lower() == "id":
                continue
            elif champ.lower() == "genre":
                index = 0 if coach_data[champ] == "Masculin" else 1
                index_genre = st.radio(champ, ["Masculin", "Feminin"], index=index)
                valeurs[champ] = "Masculin" if index_genre else "Feminin"
            elif champ.lower() == "date_naissance":
                valeurs[champ] = st.date_input(champ, value=coach_data[champ])
            elif champ.lower() == "horaire":
                valeurs[champ] = st.date_input(champ)
            else:
                valeurs[champ] = st.text_input(f"{champ}", value=coach_data[champ])

        col1, col2 = st.columns(2)
        with col1:
            mettre_a_jour = st.form_submit_button("Mettre à jour")
        with col2:
            annuler = st.form_submit_button("Annuler")
            
        if annuler:
            return "annuler"
        elif mettre_a_jour:
            return valeurs
    return None

######################################################################

def supprimer_entree(nom_classe, db_index) :
    if 'boutons_confirmation' not in st.session_state:
        st.session_state.boutons_confirmation = False
    if st.button("Supprimer", key="bouton_suprimer"):
        st.session_state.afficher_form_ajout = False
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

if 'afficher_form_ajout' not in st.session_state:
    st.session_state.afficher_form_ajout = False
    
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
    donnees_brutes = selectionner_donnees(nom_classe)
    liste_donnees = []
    
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
        fonction_format = lambda x: f"{df_donnees.loc[x, 'id_membre']} {df_donnees.loc[x, 'id_cours']} {df_donnees.loc[x, 'date_inscription']}"
    elif nom_classe == Membre : 
        fonction_format = lambda x: f"{df_donnees.loc[x, 'prenom']} {df_donnees.loc[x, 'nom']}  |  téléphone : {df_donnees.loc[x, 'telephone']}"
        
    index_selection_donnee = st.selectbox(
        f"Sélectionnez un(e) {nom_classe.__str__()} à modifier ou supprimer :",df_donnees.index,format_func=fonction_format)
    
    db_index_donnee = int(df_donnees.loc[index_selection_donnee, 'id'])
    
    if db_index_donnee is not None and db_index_donnee is not None:
        # st.write(f"Vous avez sélectionné le cours : {df_donnees.loc[db_index_donnee, 'sport']} à {df_donnees.loc[db_index_donnee, 'horaire']}")
        col1, col2, col3 = st.columns(3)
        
        # bouton ajouter
        with col1 :
            if st.button("Ajouter", key="bouton_ajouter"):
                st.session_state.afficher_form_ajout = True
                st.session_state.afficher_form_modifier = False
        if st.session_state.afficher_form_ajout:
            nouvelles_donnees = nouveau_form(liste_champs)
            
            if nouvelles_donnees  == "annuler" :
                st.session_state.afficher_form_ajout = False
                st.rerun()
            elif nouvelles_donnees is not None :
                inserer_donnees(nouvelles_donnees, nom_classe)
                st.success(f"{nom_classe} ajouté(e) avec succès")
                st.session_state.afficher_form_ajout = False
                time.sleep(2)
                st.rerun()
                
        # bouton de modification
        with col2:
            if st.button("Modifier", key="bouton_modifier"):
                st.session_state.afficher_form_modifier = True
                st.session_state.afficher_form_ajout = False

        if st.session_state.afficher_form_modifier:
            coach_data = df_donnees.loc[index_selection_donnee].to_dict()
            coach_modifs = modifier_form(coach_data)
  
            if coach_modifs == "annuler" :
                st.session_state.afficher_form_modifier = False
                st.rerun()
            elif coach_modifs is not None:
                for champ, nouvelle_valeur in coach_modifs.items():
                    modifier_donnee(Cours, db_index_donnee, champ, nouvelle_valeur)
                st.success("Coach modifié avec succès")
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
    liste_champs = ["id", "sport", "horaire", "capacite_max", "nombre_inscrits", "coach_id"]
    gestion(Cours, liste_champs)

elif add_radio == "Gérer les inscriptions" : 
    liste_champs = ["id", "id_membre", "id_cours", "date_inscription"]
    gestion(Inscription, liste_champs)
    
elif add_radio == "Gérer Membres" : 
    liste_champs = ["id", "prenom", "nom", "genre", "date_naissance", "email", "telephone", "id_carteAcces"]
    gestion(Membre, liste_champs)