from django.shortcuts import render,redirect,get_object_or_404
from .models import Medecins,Exams,Rendezvous,Patients,Ordonnances,Profile
from django.contrib.auth import authenticate, login as auth_login,logout
from .forms import RendezVousForm, ProfilePictureForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import re

######################
#definition des root de toutes les pages
def about(request):
    return render(request, 'about.html')

@login_required
def paiement_echec(request):
    return render(request, 'paiement_echec.html')

@login_required
def personnel(request):
    return render(request, 'personnel.html')

@login_required
def pharmacie(request):
    return render(request, 'pharmacie.html')

def register_doctor(request):
    return render(request, 'register_like_doctor.html')

@login_required
def paiement_reussi(request):
    return render(request, 'paiement_reussi.html')

def setting(request):
    return render(request, 'setting.html')

def call_généraliste(request):
    return render(request, 'call_généraliste.html')

def call_specialiste(request):
    return render(request, 'call_specialiste.html')

def contact(request):
    return render(request, 'contact_us.html')

#######################
#Profil utilisateur
def profil(request):
    patient = get_object_or_404(Patients, user=request.user)  # Utilisation de la relation OneToOne avec user
    return render(request, 'profil.html', {'patient': patient})


########################
#affichage des medecins
@login_required
def specialiste(request):
    medecins = Medecins.objects.all()
    return render(request, 'specialiste.html', {'medecins': medecins})

@login_required
def generaliste(request):
    medecins = Medecins.objects.all()
    return render(request, 'generaliste.html', {'medecins': medecins})

########################
# Deconnexion
def logoutuser(request):
    logout(request)
    messages.success(request, 'tu es maintenant deconnecte')
    return redirect('login')

#########################
# affichage de a page des examens
@login_required
def exams(request):
    exams = Exams.objects.all()
    return render(request, 'exams.html', {'exams': exams})

########################
# gestion de l'historique
@login_required
def historique(request):
    # Récupérer l'ID du patient connecté (associé à l'utilisateur)
    patient_id = request.user.id

    # Filtrer les rendez-vous par patient
    rendezvous_list = Rendezvous.objects.filter(patient_id=patient_id)
    ordonnance = Ordonnances.objects.filter(patient_id=patient_id)   
    # Contexte pour le template
    context = {
        'rendezvous_list': rendezvous_list,
        'ordonnance' : ordonnance
    }
    return render(request, 'historique.html', context)

######################
# Suppression d'ordonnance
def delete_ordonnance(request, ordonnance_id):
    ordonnance = get_object_or_404(Ordonnances, id=ordonnance_id, patient=request.user.id)
    ordonnance.delete()
    messages.success(request, "L'ordonnance a été supprimée avec succès.")
    return redirect('historique')

################################
#gestion des examens
@login_required    
def exams_option(request, id):   
    element = Exams.objects.get(id=id)
    exams = Exams.objects.all()    
    return render(request, 'exams_option.html', {'element':element, 'exams': exams})
# ajout de la valeur 2000 pour le deplacement sur la page examen
def deplacement(request, id):
    element = Exams.objects.get(id=id)
    if request.method == "POST":
        deplacement = 'labo_switch' in request.POST # Vérifier si la checkbox est cochée
        if deplacement == False:
            element.deplacement = 0   # Met à jour le montant de déplacement
            element.total = element.prix + element.deplacement 
            element.save()
            return redirect('exams_option', id=id)
        
        else:  
            element.deplacement = 2000  # Met à jour le montant de déplacement
            element.total = element.prix + element.deplacement  # Calcule le total
            element.save()  # Enregistre les modifications
            return redirect('exams_option', id=id)  # Redirige après la sauvegarde
                 
    return render(request, 'exams_option.html', {'element':element})


#######################
# operation d'ajout, de modification et de suppression des medecin
def add_or_update_medecin(request, id=None):
    if id:  # Si un ID est passé, on récupère le médecin pour la modification
        medecin = Medecins.objects.get(id=id)
    else:  # Sinon, c'est un ajout
        medecin = None
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('nom')
        specialite = request.POST.get('specialite')
        email = request.POST.get('email')
        photo = request.POST.get('photo')
        age = request.POST.get('age')
        
        if nom and specialite and email and photo and age:
            if medecin:  # Si on modifie un médecin existant
                medecin.nom = nom
                medecin.specialite = specialite
                medecin.email = email
                medecin.photo = photo
                medecin.age = age
                medecin.save()  # Sauvegarde des modifications
            else:  # Sinon, on ajoute un nouveau médecin
                Medecins.objects.create(nom=nom, specialite=specialite, email=email, photo=photo, age=age)

            return redirect('add_medecin')  # Redirection vers la liste après l'ajout ou la modification
    
    # Récupérer tous les médecins pour l'affichage dans le tableau
    medecins = Medecins.objects.all()
    return render(request, 'ajout_medecin.html', {'medecins': medecins, 'medecin': medecin})

def delete_medecin(request, id):
    remove = Medecins.objects.get(id=id)
    if remove:
        remove.delete()
        return redirect('add_medecin')
    return render(request, "",{'id':remove})

def update_medecin(request, id):
        update = Medecins.objects.get(id=id)
        if request.method  == 'POST':
            update.nom = request.POST.get('nom')
            update.specialite = request.POST.get('specialite')
            update.email = request.POST.get('email')
            update.photo = request.POST.get('photo')
            update.age = request.POST.get('age')
            update.save()
            return redirect("add_medecin")
        return render(request, 'ajout_medecin.html', {'medecin' : update}) 
    
#######################
#page d'ajout, de modifications et de suppression des examens
def add_or_update_exams(request, id=None):
    if id:  # Si un ID est passé, on récupère l'examen pour la modification
        exam = Exams.objects.get(id=id)
    else:  # Sinon, c'est un ajout
        exam = None
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('nom')
        prix = request.POST.get('prix')
        photo = request.POST.get('photo')
        
        
        if nom and prix :
            if exam:  # Si on modifie un examen existant
                exam.nom = nom
                exam.prix = prix
                exam.photo = photo
                exam.save()  # Sauvegarde des modifications
            else:  # Sinon, on ajoute un nouveau médecin
                Exams.objects.create(nom=nom, prix=prix, photo =photo)

            return redirect('add_exam')  # Redirection vers la liste après l'ajout ou la modification
    
    # Récupérer tous les médecins pour l'affichage dans le tableau
    exams = Exams.objects.all()
    return render(request, 'ajout_exam.html', {'exams': exams, 'exam': exam})

def delete_exam(request, id):
    remove = Exams.objects.get(id=id)
    if remove:
        remove.delete()
        return redirect('add_exam')
    return render(request, "",{'id':remove})

def update_exam(request, id):
        update = Exams.objects.get(id=id)
        if request.method  == 'POST':
            update.nom = request.POST.get('nom')
            update.prix = request.POST.get('prix')
            update.photo = request.POST.get('photo')
            update.save()
            return redirect("add_exam")
        return render(request, 'ajout_exam.html', {'exam' : update}) 
    
#######################
# prise de rendezvous et appel consultation video
@login_required
def consultation(request, id):
    print(f"User is authenticated: {request.user.is_authenticated}")  # Pour le débogage
    # Récupération du médecin par son ID
    medecin = get_object_or_404(Medecins, id=id)
    
    # Récupérer l'ID du patient à partir de l'utilisateur connecté
    patient_id = request.user.id  # On utilise l'ID de l'utilisateur connecté
    print("l'id du patient est:", patient_id)
    form = RendezVousForm(request.POST or None)

    # Gérer la réservation du rendez-vous
    if request.method == 'POST' and form.is_valid():
        jour = form.cleaned_data['jour']
        heure = form.cleaned_data['heure']

        # Vérifiez si le créneau est déjà réservé
        if Rendezvous.objects.filter(medecin=medecin, jour=jour, heure=heure).exists():
            messages.error(request, "Ce créneau est déjà réservé. Veuillez en choisir un autre.")
        else:
            # Création d'une nouvelle instance de rendez-vous
            rendez_vous = form.save(commit=False)
            rendez_vous.medecin = medecin
            rendez_vous.patient_id = patient_id  # Stocker l'ID du patient ici
            rendez_vous.save()
            messages.success(request, "Rendez-vous réservé avec succès!")
            return redirect('consultation_option_specialiste', id=id)

    # Convertir les rendez-vous réservés en un dictionnaire avec des clés formatées "jour-heure"
    rendezvous_liste = Rendezvous.objects.filter(medecin=medecin)
    appointments = {f"{rdv.jour}-{rdv.heure.strftime('%H:%M')}": True for rdv in rendezvous_liste}

    # Passer les jours et heures pour afficher un calendrier
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
    heures = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00']

    # Context pour le template
    context = {
        'medecin': medecin,
        'form': form,
        'jours': jours,
        'heures': heures,
        'appointments': appointments,
    }
    return render(request, 'consultation_option_spé.html', context)

@login_required
def delete_rendezvous(request, medecin_id, jour, heure):
    # Rechercher le médecin
    medecin = get_object_or_404(Medecins, id=medecin_id)
       # Récupérer l'ID du patient connecté (associé à l'utilisateur)
    patient_id = request.user.id

    # Filtrer les rendez-vous par patient
    rendez_vous = Rendezvous.objects.filter(medecin=medecin, patient_id=patient_id, jour=jour, heure=heure).first()
    if rendez_vous:
        # Supprimer le rendez-vous
        rendez_vous.delete()
        messages.success(request, "Le rendez-vous a été annulé avec succès.")
    else :
        messages.success(request, "Vous ne pouvez supprimer ce car ce n'est pas un rendez vous que vous avez reservé")
    # Rediriger vers la page de consultation du médecin
    return redirect('consultation_option_specialiste', id=medecin_id)

#######################
#soumission d'ordonnace
@login_required
def soumis_ordonnance(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        fichier = request.FILES.get('fichier')
        commentaire = request.POST.get('commentaire')
        patient_id = request.user.id
        
        # Vérifier que les champs requis sont fournis
        if fichier and commentaire:
            # Créer une nouvelle instance d'Ordonnances et sauvegarder
            Ordonnances.objects.create(fichier=fichier, commentaire=commentaire, patient_id=patient_id)
            return redirect('soumission_ordonnance')
    
    # Récupérer toutes les ordonnances pour les afficher dans le tableau (si nécessaire)
    ordonnances = Ordonnances.objects.all()
    return render(request, 'soumission_ordonnance.html', {'ordonnances': ordonnances})


#######################
# page d'enregistrement(register)
def register(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom_prenom = request.POST.get('nom_prenom')
        username = request.POST.get('username')
        age = request.POST.get('age')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Mot de passe avec une majuscule, minuscule, chiffre, et minimum 8 caractères
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

        # Validation de la présence de toutes les données
        if nom_prenom and username and age and telephone and email and password:
            # Vérification de la force du mot de passe
            if not re.match(password_regex, password):
                messages.error(request, "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, et un chiffre.")
                return render(request, 'register.html')
            
            # Création de l'utilisateur dans le modèle User
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                # Création du profil patient associé
                patient = Patients.objects.create(
                    user=user,
                    nom_prenom=nom_prenom,
                    age=int(age),
                    telephone=int(telephone),
                    email=email
                )
                messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
                return redirect('login')  # Redirection vers la page de connexion

            except Exception as e:
                messages.error(request, f"Erreur lors de l'inscription : {str(e)}")
                return render(request, 'register.html')

    return render(request, 'register.html')

#######################
#page de connexion(login)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentification de l'utilisateur
        user = authenticate(request, username=username, password=password)

        # Vérifiez que l'utilisateur existe et qu'il est bien un patient
        if user is not None:
            try:
                # Vérifier si l'utilisateur authentifié est dans la table Patients
                patient = Patients.objects.get(user=user)  # Relier l’utilisateur au modèle `Patients`
            except Patients.DoesNotExist:
                patient = None

            if patient:
                # Si l'utilisateur est un patient, on le connecte
                auth_login(request, user)  # Connecter l'utilisateur
                messages.success(request, "Connexion réussie. Bienvenue!")
                return redirect('home')  # Rediriger vers la page d'accueil
            else:
                messages.error(request, "Cet utilisateur n'est pas enregistré en tant que patient.")
                return redirect('login')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login.html')


#######################
# page d'acceuil
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



@login_required
def update_profile_picture(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profil')  # Redirige vers la page de profil après la mise à jour
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'profil.html', {'form': form, 'user': request.user})