from django.shortcuts import render,redirect,get_object_or_404
from .models import Medecins,Exams,Rendezvous,Patients,Ordonnances,Profile,Consultation
from django.contrib.auth import authenticate, login as auth_login,logout
from .forms import RendezVousForm, ProfilePictureForm, MedicalForm, SYMPTOM_CATEGORIES 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
import re


def admin_required(user):
    return user.is_superuser

#############################################################################################################
#definition des root de toutes les pages
def about(request):
    return render(request, 'about.html')

@login_required
def paiement_echec(request):
    return render(request, 'paiement_echec.html')

@login_required
def pharmacie(request):
    return render(request, 'pharmacie.html')

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

#############################################################################################################
#Affiche des patients:
@login_required
def rendezvous(request):
    try:
        medecin = Medecins.objects.get(user=request.user)
    except Medecins.DoesNotExist:
        messages.error(request, "Accès refusé. Cette page est réservée aux médecins.")
        return redirect('login')

    # Récupérer les patients ayant un rendez-vous avec le médecin connecté
    patients_ids = Rendezvous.objects.filter(medecin=medecin).values_list('patient_id', flat=True).distinct()
    patients = Patients.objects.filter(id__in=patients_ids)
    
    # Créer une liste de dictionnaires associant les patients à leurs rendez-vous
    patients_rendezvous = []
    for patient in patients:
        rendezvous = Rendezvous.objects.filter(medecin=medecin, patient=patient)
        patients_rendezvous.append({'patient': patient, 'rendezvous': rendezvous})

    return render(request, 'rendezvous.html', {
        'patients_rendezvous': patients_rendezvous,
        'medecin': medecin  # Transmettre l'objet médecin au template
    })

#############################################################################################################
#Profil utilisateur
def profil(request):
    patient = get_object_or_404(Patients, user=request.user)  # Utilisation de la relation OneToOne avec user
    return render(request, 'profil.html', {'patient': patient})

#############################################################################################################
#affichage des medecins
@login_required
def generaliste(request):
    # Afficher uniquement les généralistes actifs
    medecins = Medecins.objects.filter(is_active=True, specialite="Généraliste")
    return render(request, 'generaliste.html', {'medecins': medecins})

@login_required
def specialiste(request):
    # Afficher uniquement les spécialistes actifs
    medecins = Medecins.objects.filter(is_active=True).exclude(specialite = "Généraliste")
    return render(request, 'specialiste.html', {'medecins': medecins})


#############################################################################################################
# Deconnexion
def logoutuser(request):
    logout(request)
    messages.success(request, 'tu es maintenant deconnecte')
    return redirect('home_patient')

#############################################################################################################
# affichage de a page des examens
@login_required
def exams(request):
    exams = Exams.objects.all()
    return render(request, 'exams.html', {'exams': exams})

#############################################################################################################
# gestion de l'historique
@login_required
def historique(request):
    # Récupérer l'ID du patient connecté (associé à l'utilisateur)
    patient_id = request.user.id

    # Filtrer les rendez-vous par patient
    rendezvous_list = Rendezvous.objects.filter(patient_id=(patient_id-2))
    ordonnance = Ordonnances.objects.filter(patient_id=patient_id)   
    # Contexte pour le template
    context = {
        'rendezvous_list': rendezvous_list,
        'ordonnance' : ordonnance
    }
    return render(request, 'historique.html', context)

#############################################################################################################
# Suppression d'ordonnance
def delete_ordonnance(request, ordonnance_id):
    ordonnance = get_object_or_404(Ordonnances, id=ordonnance_id, patient=request.user.id)
    ordonnance.delete()
    messages.success(request, "L'ordonnance a été supprimée avec succès.")
    return redirect('historique')

#############################################################################################################
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


#########################################################################################################
# operation d'ajout, de modification et de suppression des medecin
@user_passes_test(admin_required)
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

@user_passes_test(admin_required)
def delete_medecin(request, id):
    remove = Medecins.objects.get(id=id)
    if remove:
        remove.delete()
        return redirect('add_medecin')
    return render(request, "",{'id':remove})

@user_passes_test(admin_required)
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
    
###################################################################################################
#page d'ajout, de modifications et de suppression des examens
@user_passes_test(admin_required)
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

@user_passes_test(admin_required)
def delete_exam(request, id):
    remove = Exams.objects.get(id=id)
    if remove:
        remove.delete()
        return redirect('add_exam')
    return render(request, "",{'id':remove})

@user_passes_test(admin_required)
def update_exam(request, id):
        update = Exams.objects.get(id=id)
        if request.method  == 'POST':
            update.nom = request.POST.get('nom')
            update.prix = request.POST.get('prix')
            update.photo = request.POST.get('photo')
            update.save()
            return redirect("add_exam")
        return render(request, 'ajout_exam.html', {'exam' : update}) 
    
#######################################################################################################
# prise de rendezvous et appel consultation video
@login_required
def consultation(request, id):
    # Récupération du médecin par son ID
    medecin = get_object_or_404(Medecins, id=id)

    # Récupérer l'objet patient associé à l'utilisateur connecté
    try:
        patient = Patients.objects.get(user=request.user)
    except Patients.DoesNotExist:
        messages.error(request, "Aucun patient associé à cet utilisateur.")
        return redirect('home_patient')  # Redirigez ou affichez un message d'erreur si nécessaire

    form = RendezVousForm(request.POST or None)

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
            rendez_vous.patient = patient  # Utiliser l'objet patient récupéré
            rendez_vous.save()
            messages.success(request, "Rendez-vous réservé avec succès!")
            return redirect('consultation_option_specialiste', id=id)

    # Création du dictionnaire des rendez-vous réservés
    rendezvous_liste = Rendezvous.objects.filter(medecin=medecin)
    appointments = {f"{rdv.jour}-{rdv.heure.strftime('%H:%M')}": True for rdv in rendezvous_liste}

    # Contexte pour le template
    context = {
        'medecin': medecin,
        'form': form,
        'jours': ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi'],
        'heures': ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00'],
        'appointments': appointments,
    }
    return render(request, 'consultation_option_spé.html', context)


#################################################################################################
#suppression des rendezvous par le patient
@login_required
def delete_rendezvous(request, medecin_id):
    # Rechercher le médecin
    medecin = get_object_or_404(Medecins, id=medecin_id)
  
    # Filtrer les rendez-vous par patient
    rendez_vous = Rendezvous.objects.filter(medecin=medecin, patient = Patients.objects.get(user=request.user)).first()
    if rendez_vous and (medecin.specialite != 'Généraliste') :
        # Supprimer le rendez-vous
        rendez_vous.delete()
        messages.success(request, "Le rendez-vous a été annulé avec succès.")
        return redirect('consultation_option_specialiste', id=medecin_id)
    
    elif rendez_vous and (medecin.specialite == 'Généraliste') :
         # Supprimer le rendez-vous
        rendez_vous.delete()
        messages.success(request, "Le rendez-vous a été annulé avec succès.")
        return redirect('consultation_option_généraliste', id=medecin_id)
    else :
        messages.success(request, "Vous ne pouvez supprimer ce car ce n'est pas un rendez vous que vous avez reservé")
    # Rediriger vers la page de consultation du médecin
    return render(request, '')
        

#suppression des rendezvous par le praticien
@login_required
def delete_rendezvous_doctor(request, rendezvous_id):
    # Vérifier si l'utilisateur connecté est un médecin
    try:
        medecin = Medecins.objects.get(user=request.user)
    except Medecins.DoesNotExist:
        messages.error(request, "Accès refusé. Cette page est réservée aux médecins.")
        return redirect('login')

    # Récupérer le rendez-vous en fonction de l'ID
    rendez_vous = get_object_or_404(Rendezvous, id=rendezvous_id, medecin=medecin)
    
    # Supprimer le rendez-vous
    rendez_vous.delete()
    messages.success(request, "Le rendez-vous a été supprimé avec succès.")

    # Redirection vers la page des rendez-vous ou la liste des patients du médecin
    return redirect('rendezvous')  # Rediriger vers la vue de la liste des patients ou une autre page du médecin

#############################################################################################################
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


#############################################################################################################
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
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'

        # Validation de la présence de toutes les données
        if nom_prenom and username and age and telephone and email and password:
            # Vérification de la force du mot de passe
            if not re.match(password_regex, password):
                messages.error(request, "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, et un chiffre.")
                return render(request, 'register.html')
            
            # Création de l'utilisateur dans le modèle User
            try:
                print("➡️ Tentative de création de l'utilisateur...")  # 🔍 Debugging
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                print("✅ Utilisateur créé :", user)  # 🔍 Debugging

                # Création du profil patient associé
                print("➡️ Tentative de création du patient...")  # 🔍 Debugging
                patient = Patients.objects.create(
                    user=user,
                    nom_prenom=nom_prenom,
                    age=int(age),
                    telephone=int(telephone),
                    email=email
                )
                print("✅ Patient créé :", patient)  # 🔍 Debugging

                messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
                return redirect('login')  # Redirection vers la page de connexion

            except Exception as e:
                print("❌ Erreur lors de l'inscription :", e)  # 🔍 Debugging
                messages.error(request, f"Erreur lors de l'inscription : {str(e)}")
                return render(request, 'register.html')

    return render(request, 'register.html')

#############################################################################################################
#page de connexion(login)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Vérifiez si l'utilisateur est un patient
            try:
                patient = Patients.objects.get(user=user)
                auth_login(request, user)
                messages.success(request, "Connexion réussie. Bienvenue!")
                return redirect('home_patient')  # Rediriger vers la page patient

            except Patients.DoesNotExist:
                pass  # Si ce n'est pas un patient, on continue pour vérifier si c'est un médecin

            # Vérifiez si l'utilisateur est un médecin
            try:
                medecin = Medecins.objects.get(user=user)
                auth_login(request, user)
                
                # Vérifiez si le médecin est inactif et affichez un message d'avertissement
                if not medecin.is_active:
                    messages.warning(request, "Votre compte est inactif, mais vous pouvez tout de même accéder au site.")
                
                # Redirection vers la page d'accueil du médecin
                messages.success(request, "Connexion réussie. Bienvenue, Docteur!")
                return redirect('home_doctor')  # Rediriger vers la page médecin

            except Medecins.DoesNotExist:
                messages.error(request, "Cet utilisateur n'est pas enregistré en tant que patient ou médecin.")
                return redirect('login')

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login.html')

#############################################################################################################
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


#############################################################################################################
# Ajout de la photo de profil
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

def register_doctor(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('firstname')
        specialite = request.POST.get('specialite')
        email = request.POST.get('email')
        age = request.POST.get('age')
        password = request.POST.get('password')
        username = request.POST.get('username')  # Assurez-vous qu'il existe un champ 'username' dans le formulaire

        # Validation du mot de passe (au moins 8 caractères, 1 majuscule, 1 minuscule, et 1 chiffre)
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        
        if not re.match(password_regex, password):
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, et un chiffre.")
            return render(request, 'register_like_doctor.html')

        # Vérification de la présence de toutes les données obligatoires
        if nom and specialite and email and age and password and username:
            try:
                # Création de l'utilisateur dans le modèle User
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Création du profil médecin associé
                medecin = Medecins.objects.create(
                    user=user,
                    nom=nom,
                    specialite=specialite,
                    email=email,
                    age=int(age)
                )
                
                messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
                return redirect('login')  # Redirection vers la page de connexion pour les médecins

            except Exception as e:
                messages.error(request, f"Erreur lors de l'inscription : {str(e)}")
                return render(request, 'register_like_doctor.html')
        
        else:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'register_like_doctor.html')

    return render(request, 'register_like_doctor.html')

#############################################################################################################
# decorateur pour restreindre l'acces aux utilisateurs qui ne sont pas des medecins a la page home_doctor
def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Vérifier que l'utilisateur est connecté et est un médecin
        if request.user.is_authenticated:
            try:
                # Essayer de récupérer l'objet Medecins correspondant à l'utilisateur connecté
                Medecins.objects.get(user=request.user)
                # Si trouvé, c'est un médecin; continuer vers la vue
                return view_func(request, *args, **kwargs)
            except Medecins.DoesNotExist:
                # Si l'utilisateur n'est pas un médecin, rediriger avec un message d'erreur
                messages.error(request, "Accès refusé. Cette page est réservée aux médecins.")
                return redirect('login')
        else:
            # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
            return redirect('login')

    return wrapper

@doctor_required
@login_required
def home_doctor(request):
    # Vue pour la page d'accueil des médecins
    return render(request, 'home_doctor.html')

################################################################################################
# Confirmation du praticien dans le systeme
@login_required
def activate_medecin(request, medecin_id):
    medecin = get_object_or_404(Medecins, id=medecin_id)
    # Alterner le statut actif
    medecin.is_active = not medecin.is_active
    medecin.save()
    status = "activé" if medecin.is_active else "désactivé"
    messages.success(request, f"Le statut de {medecin.nom} a été {status}.")
    return redirect('add_medecin')  # Redirigez vers la liste des médecins (ou autre page d'administration)

######################################################################################################
def enregistrer_consultation(request, medecin_id, consultation_type):
    # Récupérer le patient connecté
    patient = get_object_or_404(Patients, user=request.user)

    # Récupérer le médecin concerné
    medecin = get_object_or_404(Medecins, id=medecin_id)

    # Créer et sauvegarder la consultation
    consultation = Consultation.objects.create(
        patient=patient,
        medecin=medecin,
        consultation_type=consultation_type,
        date_enregistrement=timezone.now()
    )

    # Redirection vers le lien de paiement
    if consultation_type == 'video':
        return redirect("https://demo.campay.net/pay/frais-de-consultation-4235-1729426350-ARK/")
    elif consultation_type == 'audio':
        return redirect("https://demo.campay.net/pay/frais-de-consultation-4235-1729426350-ARK/")
    
@login_required
def medecin_consultations(request):
    try:
        # Récupérer le médecin connecté
        medecin = Medecins.objects.get(user=request.user)
    except Medecins.DoesNotExist:
        # Si l'utilisateur n'est pas un médecin, rediriger ou afficher un message
        messages.error(request, "Accès refusé. Cette page est réservée aux médecins.")
        return redirect('login')

    # Récupérer les consultations associées au médecin
    consultations = Consultation.objects.filter(medecin=medecin).order_by('-date_enregistrement')

    # Passer les consultations au template
    return render(request, 'medecin_consultations.html', {'consultations': consultations, 'medecin': medecin})



def diagnostic_view(request):
    selected_body_part = None

    if request.method == "POST":
        selected_body_part = request.POST.get("body_part")  # Récupère la partie du corps sélectionnée
        form = MedicalForm(request.POST, selected_body_part=selected_body_part)
        
        if form.is_valid():
            return render(request, 'result.html', {'data': form.cleaned_data})
    
    else:
        form = MedicalForm()

    return render(request, 'questionnaire.html', {'form': form, 'selected_body_part': selected_body_part})

