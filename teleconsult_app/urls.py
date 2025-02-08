from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home_patient'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('about/', views.about, name='about'),
    path('generaliste/', views.generaliste, name='generaliste'),
    path('specialiste/', views.specialiste, name='specialiste'),
    path('call_généraliste/', views.call_généraliste, name='call_généraliste'), 
    path('call_specialiste/', views.call_specialiste, name='call_specialiste'), 
    path('consultation_option_généraliste/<int:id>/', views.consultation, name='consultation_option_généraliste'),
    path('consultation_option_specialiste/<int:id>/', views.consultation, name='consultation_option_specialiste'),
    path('contact/', views.contact, name='contact'),
    path('exams_option/<int:id>/', views.exams_option, name='exams_option'),
    path('exams/', views.exams, name='exams'),
    path('historique/', views.historique, name='historique'),
    path('login/', views.login, name='login'),
    path('paiement_echec/', views.paiement_echec, name='paiement_echec'),
    path('paiement_reussi/', views.paiement_reussi, name='paiement_reussi'),
    path('pharmacie/', views.pharmacie, name='pharmacie'), 
    path('register/', views.register, name='register'), 
    path('setting/', views.setting, name='setting'),
    path('soumission_ordonnance/', views.soumis_ordonnance, name='soumission_ordonnance'), 
    path('deplacement/<int:id>/', views.deplacement, name='deplacement'),
    path('delete_rendezvous/<int:medecin_id>/', views.delete_rendezvous, name='delete_rendezvous'),
    path('delete_rendezvous_doctor/<int:rendezvous_id>/', views.delete_rendezvous_doctor, name='delete_rendezvous_doctor'),
    path('delete_ordonnance/<int:ordonnance_id>/', views.delete_ordonnance, name='delete_ordonnance'),
    path('profil/', views.profil, name='profil'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('home/doctor/', views.home_doctor, name='home_doctor'),
    path('activate_medecin/<int:medecin_id>/', views.activate_medecin, name='activate_medecin'),
    path('rendezvous/', views.rendezvous, name='rendezvous'),
    path('consultation/<int:medecin_id>/<str:consultation_type>/', views.enregistrer_consultation, name='enregistrer_consultation'),
    path('mes_consultations/', views.medecin_consultations, name='medecin_consultations'),
    path('diagnostic/', views.diagnostic_view, name='diagnostic'),

    ######################
    #action sur le medecin
    path("add_medecin/", views.add_or_update_medecin, name="add_medecin"),
    path("update_medecin/<int:id>/", views.add_or_update_medecin, name="update_medecin"), 
    path("delete_medecin/<int:id>/", views.delete_medecin, name="delete_medecin"),
    ######################
    #action sur l'examen
    path("add_exam/", views.add_or_update_exams, name="add_exam"),
    path("update_exam/<int:id>/", views.add_or_update_exams, name="update_exam"), 
    path("delete_exam/<int:id>/", views.delete_exam, name="delete_exam"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)