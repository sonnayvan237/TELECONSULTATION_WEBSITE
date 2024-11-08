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
