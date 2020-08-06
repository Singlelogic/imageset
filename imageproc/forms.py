from django import forms

from .models import Images


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image_url', 'image']

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ImageSize(forms.Form):
    width = forms.IntegerField(label='Ширина')
    height = forms.IntegerField(label='Высота')
