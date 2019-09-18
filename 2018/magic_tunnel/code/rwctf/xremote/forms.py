from django import forms

from . import models


class ImageForm(forms.Form):
    url = forms.CharField(max_length=512, widget=forms.URLInput())
