from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Truck, County, Feature, Image
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from dal import autocomplete


ImageFormSet = inlineformset_factory(Truck, Image, fields=['image'], extra=3, can_delete=True)


class TruckForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(queryset=Feature.objects.distinct(), widget=forms.CheckboxSelectMultiple,
                                     to_field_name='name')
    county = forms.ModelChoiceField(
        queryset=County.objects.all(),
        widget=autocomplete.ModelSelect2(url='trucks:county-autocomplete')
    )


    def clean(self):
        features = self.cleaned_data.get('features')
        print (features)

    class Meta:
        model = Truck
        fields = ('county', 'name', 'status', 'door', 'engine_size', 'gearbox',  'fuel_type', 'picture', 'year', 'price', 'make', 'model','mileage', 'seat', 'color', 'tags', 'availability',
                                      'description', 'features')