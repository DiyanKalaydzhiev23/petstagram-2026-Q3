from django import forms
from photos.models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = "__all__"


class PhotoAddForm(PhotoForm):
    ...


class PhotoEditForm(PhotoForm):
    ...
