import streamlit as st
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="La Poigne d'Acier - Accueil",
    page_icon="💪",
    layout="wide"
)

# Chargement de l'image
image_path = "image1.webp"  # Remplacez par le chemin correct si l'image est ailleurs
try:
    image = Image.open(image_path)
except FileNotFoundError:
    st.error("L'image 'image1.jpg' n'a pas été trouvée. Assurez-vous qu'elle est dans le bon répertoire.")

# Titre principal
st.title("💪 Bienvenue à La Poigne d'Acier 💪")

# Description
st.markdown("""
**La Poigne d’Acier**, la salle de sport qui ne fait pas dans la demi-mesure, est un lieu emblématique pour les passionnés de fitness, de musculation et de boxe. Située en plein cœur de la ville, elle propose un large éventail de cours pour satisfaire tous les niveaux et objectifs, que vous souhaitiez :
- Sculpter votre corps
- Gagner en force et en endurance
- Évacuer le stress de la journée
""")

# Affichage de l'image d'accueil
if 'image' in locals():
    st.image(image, caption="Bienvenue à La Poigne d'Acier")

# Sous-titre pour les cours proposés
st.subheader("🏋️‍♂️ Cours proposés :")

# Liste des cours
st.markdown("""
- **Fitness** : Améliorez votre condition physique générale avec des séances dynamiques.
- **Musculation** : Développez votre force et vos muscles grâce à un accompagnement personnalisé.
- **Boxe** : Apprenez à canaliser votre énergie et perfectionnez votre technique.
- **Cours collectifs** : Renforcez votre motivation en groupe.
- **Yoga Stretch** : Combinez relaxation et assouplissement pour un bien-être total.
""")

# Footer
st.markdown("---")
st.markdown("👊 **Prêt à relever le défi ?** Venez nous rejoindre et découvrez tout ce que **La Poigne d'Acier** a à offrir !")

# Contact
st.sidebar.title("📬 Contactez-nous")
st.sidebar.markdown("""
- 📍 **Adresse** : 123 Rue du Muscle, BATATA City
- 📞 **Téléphone** : +33 1 23 45 67 89
- 📧 **Email** : contact@lapoignedacier.com
""")
