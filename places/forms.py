from django import forms

class PlaceForm(forms.Form):
    name = forms.CharField(label='Назва', max_length=100)
    full_description = forms.CharField(label='Повний опис', widget=forms.Textarea, required=False)
    type = forms.CharField(label='Тип місця', max_length=50, required=False)
    location = forms.CharField(label='Локація (залишити пустою = Secret place)', max_length=200, required=False)
    rating = forms.IntegerField(label='Рейтинг (1-5)', min_value=1, max_value=5)
