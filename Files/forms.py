from django.forms import forms


class FileLoadForm(forms.Form):
    file = forms.FileField()
