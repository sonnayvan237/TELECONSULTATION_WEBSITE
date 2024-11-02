from django import forms
from .models import Rendezvous

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
