from django import forms
from .models import Subscriber

class SubscriberForm(forms.Form):
    email = forms.EmailField(required=True)
