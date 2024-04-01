from django import forms

class GenForm(forms.Form):
    url = forms.CharField(max_length=100)