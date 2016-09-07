from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget
from .models import Events
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class EventForm(forms.ModelForm):
    event_time = forms.DateTimeField()

    class Meta:
        model = Events
        fields = [
            'title',
            'location',
            'band',
            'event_time',
            'member_tickets_price',
            'normal_tickets_price',
        ]
        widgets = {
            'event_time': AdminDateWidget()
        }
