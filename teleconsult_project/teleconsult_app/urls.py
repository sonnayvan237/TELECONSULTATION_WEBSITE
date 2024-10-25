from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('generaliste/', views.generaliste, name='generaliste'), 
    path('specialiste/', views.specialiste, name='specialiste'),
    path('call_généraliste/', views.call_généraliste, name='call_généraliste'), 
    path('call_specialiste/', views.call_specialiste, name='call_specialiste'), 
    path('consultation_option_généraliste/', views.consultation_option_généraliste, name='consultation_option_généraliste'),
    path('consultation_option_specialiste/', views.consultation_option_specialiste, name='consultation_option_specialiste'),
    path('contact/', views.contact, name='contact'),
    path('exams_option/', views.exams_option, name='exams_option'),
    path('exams/', views.exams, name='exams'),
    path('historique/', views.historique, name='historique'),
    path('login/', views.login, name='login'),
    path('paiement_echec/', views.paiement_echec, name='paiement_echec'),
    path('paiement_reussi/', views.paiement_reussi, name='paiement_reussi'),
    path('personnel/', views.personnel, name='personnel'), 
    path('pharmacie/', views.pharmacie, name='pharmacie'), 
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('register/', views.register, name='register'), 
    path('setting/', views.setting, name='setting'),
    path('soumission_ordonnance/', views.soumis_ordonnance, name='soumission_ordonnance'), 
    
    # Ajoutez d'autres URL ici
]
