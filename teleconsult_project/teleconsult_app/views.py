from django.shortcuts import render,HttpResponse

# Create your views here.
def about(request):
    return render(request, 'about.html')

def generaliste(request):
    return render(request, 'generaliste.html')

def specialiste(request):
    return render(request, 'specialiste.html')

def call_généraliste(request):
    return render(request, 'call_généraliste.html')

def call_specialiste(request):
    return render(request, 'call_specialiste.html')

def consultation_option_généraliste(request):
    return render(request, 'consultation_option_géné.html')

def consultation_option_specialiste(request):
    return render(request, 'consultation_option_spé.html')

def contact(request):
    return render(request, 'contact_us.html')
    # return HttpResponse(str([1,3,4]))

def exams_option(request):
    return render(request, 'exams_option.html')

def exams(request):
    return render(request, 'exams.html')

def historique(request):
    return render(request, 'historique.html')

def login(request):
    return render(request, 'login.html')

def paiement_echec(request):
    return render(request, 'paiement_echec.html')

def personnel(request):
    return render(request, 'personnel.html')

def pharmacie(request):
    return render(request, 'pharmacie.html')

def register_doctor(request):
    return render(request, 'register_like_doctor.html')

def paiement_reussi(request):
    return render(request, 'paiement_reussi.html')

def register(request):
    return render(request, 'register.html')

def setting(request):
    return render(request, 'setting.html')

def soumis_ordonnance(request):
    return render(request, 'soumis_ordonnance.html')


def home(request):
    services = [
        {
            "url": "specialiste",
            "image": "images/visite-chez-le-medecin.png",
            "title": "Consultations Médicales",
            "description": "Accès à des médecins généralistes et spécialistes pour des consultations à distance via appel vidéo, audio ou chat.",
        },
        {
            "url": "soumission_ordonnance",
            "image": "images/dossier-medical.png",
            "title": "Prescription Médicale",
            "description": "Vous pouvez soumettre vos ordonnances, et obtenir des prescriptions à distance, si nécessaire.",
        },
        {
            "url": "contact",
            "image": "images/medical.png",
            "title": "Références à des Spécialiste",
            "description": "Contactez nous si nécessaire pour une orientation vers des spécialistes agrées pour des consultations en personne.",
        },
        {
            "url": "historique",
            "image": "images/patient.png",
            "title": "Accès à des Dossiers Médicaux",
            "description": "Consultez votre historique de consultation et suivez l'évolution de votre traitement en temps réel.",
        }
    ]
  
    daily_health_tips = [
        {
            "image": "images/calendrier.png",
            "title": "Accedez aux soins plus facilement",
            "description": "Réservez des consultations vidéo ou en présentiel, et recevez des rappels pour ne jamais les manquer.",
        },
        {
            "image": "images/battement-de-coeur.png",
            "title": "Gérez votre santé",
            "description": "Rassemblez facilement toutes vos informations de santé et celles de ceux qui comptent pour nous.",
        },
        {
            "image": "images/megaphone.png",
            "title": "Bénéficiez de soins personnalisés",
            "description": "Echangez avec vos praticiens par message, obtenez des conseils préventifs et recevez des soins quand vous en avez besoin.",
        }
    ]
    
    engagements = [
        {
            "title": "Confidentialité des Données",
            "description": "Nous prenons des mesures rigoureuses pour protéger la confidentialité de vos informations personnelles et médicales. Toutes les consultations se déroulent dans un environnement sécurisé, et vos données sont cryptées pour éviter tout accès non autorisé.",
            "image": "images/cercle.png",
        },
        {
            "title": "Professionnalisme",
            "description": "Nos professionnels de santé sont qualifiés, certifiés et respectent les normes les plus élevées en matière de pratique médicale. Ils s'engagent à vous offrir des conseils et des soins basés sur les meilleures pratiques médicales.",
            "image": "images/cercle.png",
        },
        {
            "title": "Sécurité des Communications",
            "description": "Les outils de téléconsultation que nous utilisons sont conçus pour garantir la sécurité des communications entre vous et votre professionnel de santé. Les sessions sont protégées par des technologies avancées.",
            "image": "images/cercle.png",
        },
        {
            "title": "Accès et Consentement",
            "description": "Vous avez le contrôle total sur vos informations médicales et la manière dont elles sont utilisées. Nous vous informons clairement des modalités d'accès et de partage de vos données, et nous obtenons votre consentement éclairé avant toute consultation.",
            "image": "images/cercle.png",
        },
        {
            "title": "Support et Assistance",
            "description": "Notre équipe est disponible pour répondre à toutes vos questions et préoccupations concernant le fonctionnement de notre service de téléconsultation. Nous nous engageons à vous fournir une assistance rapide et efficace.",
            "image": "images/cercle.png",
        },
        {
            "title": "Amélioration Continue",
            "description": "Nous nous engageons à améliorer continuellement nos services en fonction de vos retours et des évolutions technologiques. Votre expérience est au cœur de notre démarche qualité.",
            "image": "images/cercle.png",
        }
    ]
    
    specialistes = [
        {
            "name": "Dr. Sarah Johnson",
            "specialty": "Anesthésiste",
            "description": "L'anesthésiste est un médecin spécialisé dans l'administration d'anesthésies pour rendre les interventions chirurgicales et médicales indolores et sécurisées. Il surveille également les fonctions vitales du patient pendant l'opération pour assurer une anesthésie efficace et sûre.",
            "image": "images/freepik-export-20240914215917iPSm.jpeg",
        },
        {
            "name": "Dr. Ahmed Silha",
            "specialty": "Dentiste",
            "description": "Le dentiste est un professionnel de la santé spécialisé dans le diagnostic, le traitement et la prévention des problèmes dentaires et bucco-dentaires. Il réalise des examens, des nettoyages, des restaurations, et des interventions chirurgicales.",
            "image": "images/freepik-export-20240914213557haM0.jpeg",
        },
        {
            "name": "Dr. Alphonse Jigo",
            "specialty": "Dermatologue",
            "description": "Le dermatologue est un médecin spécialisé dans le diagnostic et le traitement des maladies de la peau, des cheveux et des ongles. Il traite des affections variées, allant des éruptions cutanées aux cancers de la peau, et fournit des conseils sur les soins de la peau.",
            "image": "images/freepik-export-20240914220341m4Bt.jpeg",
        },
        {
            "name": "Dr. Alice Rose",
            "specialty": "Cardiologue",
            "description": "Le cardiologue diagnostique et traite les maladies du cœur et des vaisseaux sanguins. Il utilise divers tests pour évaluer la fonction cardiaque et gère les conditions comme l'hypertension et l'insuffisance cardiaque.",
            "image": "images/freepik-export-20240915180649lZwS.jpeg",
        },
    ]
    return render(request, 'home.html', {'daily_health_tips': daily_health_tips,'services': services, 'engagements': engagements, 'specialistes': specialistes})