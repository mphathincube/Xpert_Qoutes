from django import forms
from .models import Client, Quote


class ClientForm(forms.ModelForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['client', 'service', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].required = False
        self.fields['client'].widget.attrs.update(
            {'class': 'select2', 'style': 'width: 100%;'})
