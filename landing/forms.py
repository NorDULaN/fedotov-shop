from django import forms
from .models import Subscriber

class SubscriberForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'почта@yandex.ru'
