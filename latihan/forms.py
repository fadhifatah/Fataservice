from django import forms


class DocumentForm(forms.Form):
    file = forms.FileField(
        label='Pick a file to be compressed'
    )
