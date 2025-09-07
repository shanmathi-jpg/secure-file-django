# fileapp/forms.py

from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(
        label='Select a file to upload',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
