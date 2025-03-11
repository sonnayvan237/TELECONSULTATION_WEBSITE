from django import forms
from .models import Rendezvous, Profile

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = Rendezvous
        fields = ['jour', 'heure']
        widgets = {
            'jour': forms.Select(choices=[
                ('lundi', 'Lundi'),
                ('mardi', 'Mardi'),
                ('mercredi', 'Mercredi'),
                ('jeudi', 'Jeudi'),
                ('vendredi', 'Vendredi')
            ]),
            'heure': forms.TimeInput(attrs={'type': 'time'})
        }


# forms.py
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

# Options de zones géographiques
GEOGRAPHIC_ZONES = [
    ("afrique", "Afrique"),
    ("amerique_nord", "Amérique du Nord"),
    ("amerique_sud", "Amérique du Sud"),
    ("asie", "Asie"),
    ("europe", "Europe"),
    ("oceanie", "Océanie")
]

# Dictionnaire des symptômes par partie du corps
SYMPTOM_CATEGORIES = {
    "Tête": [
        "Maux de tête", "Migraine", "Vertiges", "Étourdissements", "Vision trouble", 
        "Douleur au cuir chevelu", "Sensibilité à la lumière", "Douleur frontale"
    ],
    "Yeux": [
        "Rougeur des yeux", "Sécheresse oculaire", "Larmoiement excessif", "Vision floue", 
        "Démangeaisons oculaires", "Sensation de corps étranger", "Sensibilité à la lumière"
    ],
    "Oreilles": [
        "Douleur à l'oreille", "Perte d'audition", "Sifflements dans l'oreille", "Acouphènes", 
        "Oreille bouchée", "Écoulement auriculaire", "Infection de l'oreille"
    ],
    "Nez et Gorge": [
        "Nez qui coule", "Congestion nasale", "Éternuements continus", "Irritation de la gorge", 
        "Douleur en avalant", "Voix enrouée", "Maux de gorge", "Sécheresse de la gorge", 
        "Saignement de nez", "Mauvaise haleine persistante"
    ],
    "Poumons et Poitrine": [
        "Douleur thoracique", "Essoufflement", "Toux persistante", "Oppression thoracique", 
        "Respiration sifflante", "Expectorations sanglantes", "Difficulté à respirer la nuit"
    ],
    "Système Digestif": [
        "Douleur abdominale", "Ballonnements", "Nausées", "Vomissements", 
        "Diarrhée", "Constipation", "Reflux acide", "Brûlures d'estomac", 
        "Selles noires ou sanglantes", "Difficulté à digérer", "Manque d'appétit"
    ],
    "Peau": [
        "Démangeaisons", "Rougeurs", "Éruptions cutanées", "Sécheresse excessive", 
        "Urticaire", "Plaques squameuses", "Ampoules", "Peau qui pèle", 
        "Gonflement sous-cutané", "Lésions suintantes", "Décoloration de la peau"
    ],
    "Muscles et Articulations": [
        "Douleurs musculaires", "Raideur articulaire", "Gonflement des articulations", 
        "Faiblesse musculaire", "Crampe musculaire", "Inflammation des tendons", 
        "Perte de mobilité", "Douleurs diffuses dans le corps"
    ],
    "Système Nerveux": [
        "Engourdissements", "Tremblements", "Convulsions", "Faiblesse musculaire soudaine", 
        "Troubles de la coordination", "Perte de mémoire", "Confusion mentale", 
        "Troubles du sommeil", "Sensation de picotements", "Vertiges fréquents"
    ],
    "Système Urinaire et Reproducteur": [
        "Douleur en urinant", "Sang dans les urines", "Incontinence", "Brûlure urinaire", 
        "Besoin fréquent d'uriner", "Douleur pelvienne", "Éjaculation douloureuse", 
        "Sécheresse vaginale", "Menstruations irrégulières", "Démangeaisons génitales"
    ],
    "Système Cardiovasculaire": [
        "Palpitations", "Hypertension", "Douleur thoracique", "Sensation de malaise", 
        "Œdème des pieds et des jambes", "Pâleur excessive", "Fatigue inexpliquée"
    ],
    "Système Endocrinien": [
        "Prise de poids soudaine", "Perte de poids inexpliquée", "Soif excessive", 
        "Transpiration excessive", "Intolérance au froid", "Troubles hormonaux"
    ],
    "Système Immunitaire": [
        "Fièvre persistante", "Ganglions lymphatiques enflés", "Fatigue chronique", 
        "Inflammation des articulations", "Sensibilité accrue aux infections"
    ],
    "Santé Mentale": [
        "Anxiété", "Dépression", "Insomnie", "Irritabilité", "Hallucinations", 
        "Crises de panique", "Perte de motivation", "Idées suicidaires"
    ]
}

# Définition des choix basés sur les valeurs uniques extraites
CHRONIC_DISEASES_CHOICES = [('', 'Sélectionnez...')] + [(d, d) for d in [
    'Arthrite rhumatoïde', 'Asthme', 'Diabète de type 2', 'Hypertension artérielle',
    'Hypothyroïdie', 'Insuffisance cardiaque', 'Maladie de Crohn', 'Maladie de Parkinson',
    'Maladie pulmonaire obstructive chronique', 'Sclérose en plaques', 'Aucun(e)'
]]

MEDICATIONS_CHOICES = [('', 'Sélectionnez...')] + [(m, m) for m in [
    'Amiodarone', 'Aspirine', 'Atorvastatine', 'Ibuprofène', 'Insuline', 'Levothyroxine',
    'Losartan', 'Metformine', 'Prednisone', 'Salbutamol', 'Aucun(e)'
]]

ALLERGIES_CHOICES = [('', 'Sélectionnez...')] + [(a, a) for a in [
    'Allergie au latex', 'Allergie aux acariens', 'Allergie aux antibiotiques', 'Allergie aux arachides',
    'Allergie aux fruits de mer', 'Allergie aux œufs', 'Allergie aux pollens',
    'Allergie aux produits laitiers', 'Aucune allergie connue', 'Aucun(e)'
]]

FAMILY_HISTORY_CHOICES = [('', 'Sélectionnez...')] + [(f, f) for f in [
    'Antécédents d’AVC', 'Antécédents d’asthme', 'Antécédents de cancer',
    'Antécédents de diabète', 'Antécédents de maladies auto-immunes',
    'Antécédents de maladies cardiovasculaires', 'Antécédents d’hypertension',
    'Antécédents d’insuffisance rénale', 'Aucun antécédent médical connu', 'Aucun(e)'
]]


class MedicalForm(forms.Form):
    age = forms.IntegerField(label="Âge", min_value=0, max_value=120, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label="Sexe", choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    body_part = forms.ChoiceField(
        label="Partie du corps affectée",
        choices=[(k, k) for k in SYMPTOM_CATEGORIES.keys()],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    symptom = forms.ChoiceField(
        label="Symptôme",
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    chronic_diseases = forms.ChoiceField(
        choices=CHRONIC_DISEASES_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Maladies chroniques",
        required=False
    )
    
    medications = forms.ChoiceField(
        choices=MEDICATIONS_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Médicaments en cours",
        required=False
    )

    lifestyle = forms.ChoiceField(label="Mode de vie", choices=[('active', 'Actif'), ('sedentary', 'Sédentaire')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    smoking = forms.ChoiceField(label="Fumeur", choices=[('yes', 'Oui'), ('no', 'Non')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    alcohol = forms.ChoiceField(label="Consommation d'alcool", choices=[('yes', 'Oui'), ('no', 'Non')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    allergies = forms.ChoiceField(
        choices=ALLERGIES_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Allergies",
        required=False
    )
    
    family_history = forms.ChoiceField(
        choices=FAMILY_HISTORY_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Antécédents familiaux de maladies",
        required=False
    )
    
    geographic_zone = forms.ChoiceField(label="Zone géographique", choices=GEOGRAPHIC_ZONES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        selected_body_part = kwargs.pop('selected_body_part', None)
        super().__init__(*args, **kwargs)
        
        # Mise à jour dynamique des symptômes
        if selected_body_part and selected_body_part in SYMPTOM_CATEGORIES:
            self.fields['symptom'].choices = [(s, s) for s in SYMPTOM_CATEGORIES[selected_body_part]]
        else:
            self.fields['symptom'].choices = [('', 'Sélectionnez une partie du corps d\'abord')]
