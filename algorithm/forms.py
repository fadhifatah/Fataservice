from django import forms


class InputForm(forms.Form):
    A = forms.CharField(label='A')
    B = forms.CharField(label='B')
    C = forms.CharField(label='C')
    D = forms.CharField(label='D')
