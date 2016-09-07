from django import forms
from .models import Genre, Bands


class BandForm(forms.ModelForm):
    class Meta:
        model = Bands
        fields = [
            'name',
            'genre',
            'booking_fee',
            'bio',
            'raider',
            'contact',
        ]
