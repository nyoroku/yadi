from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Vehicle, Image, County, Model, Make
from django.db import transaction
from .models import Profile, Private, User, Feature, Service, Quote, Offer
from phonenumber_field.formfields import PhoneNumberField
from dal import autocomplete


ImageFormSet = inlineformset_factory(Vehicle, Image, fields=['title', 'image'], extra=3, can_delete=True)


class ProfileForm(forms.ModelForm):
    COUNTY = (('kirinyaga', 'Kirinyaga'),
              ('nairobi', 'Nairobi'),
              ('mombasa', 'Mombasa')

              )
    company = forms.CharField(max_length=50)
    county = forms.ChoiceField(choices=COUNTY)
    number = PhoneNumberField(help_text='Please include the country code e.g +254', label='Phone Number')

    class Meta:
        model = Profile
        fields = ('county', 'company', 'number')

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)

        if commit:
            profile.save()

        return profile


class DealerSignUPForm(forms.ModelForm):
    email = forms.EmailField(max_length=80, help_text='Required. Use a valid Email', label='Email')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput, help_text='Passwords should match')
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput, help_text='Passwords should match')
    COUNTY = (('kirinyaga', 'Kirinyaga'),
              ('nairobi', 'Nairobi'),
              ('mombasa', 'Mombasa')

              )
    company = forms.CharField(max_length=50)
    county = forms.ChoiceField(choices=COUNTY)
    number = PhoneNumberField(help_text='Please include the country code e.g +254', label='Phone Number')
    service = forms.ModelMultipleChoiceField(queryset=Service.objects.distinct(), widget=forms.CheckboxSelectMultiple,
                                              to_field_name='name')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',  'password1', 'password2')

    def save(self, commit=True):
        user = super(DealerSignUPForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_profile = True
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            profile.company = self.cleaned_data['company']
            profile.county = self.cleaned_data['county']
            profile.number = self.cleaned_data['number']
            profile.service = self.cleaned_data['service']
            profile.save()

        return user


class PrivateSignUPForm(forms.ModelForm):
    email = forms.EmailField(max_length=80, help_text='Required. Use a valid Email', label='Email')
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput, help_text='Passwords should match')
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput, help_text='Passwords should match')
    COUNTY = (('kirinyaga', 'Kirinyaga'),
              ('nairobi', 'Nairobi'),
              ('mombasa', 'Mombasa')

              )

    county = forms.ChoiceField(choices=COUNTY)
    number = PhoneNumberField(help_text='Please include the country code e.g +254', label='Phone Number')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',  'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super(PrivateSignUPForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_private = True
        if commit:
            user.save()
            private = Private.objects.create(user=user)
            private.county = self.cleaned_data['county']
            private.number = self.cleaned_data['number']
            private.save()

        return user


class ProfileEditForm(forms.ModelForm):
    service = forms.ModelMultipleChoiceField(queryset=Service.objects.distinct(),
                                             widget=forms.CheckboxSelectMultiple,
                                             to_field_name='name')

    class Meta:
        model = Profile
        fields = ('picture', 'company', 'county', 'logo', 'number', 'description',  'service')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class PrivateEditForm(forms.ModelForm):
    class Meta:
        model = Private
        fields = ('number', 'county')


class VehicleForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(queryset=Feature.objects.distinct(), widget=forms.CheckboxSelectMultiple,
                                     to_field_name='name')
    county = forms.ModelChoiceField(
        queryset=County.objects.all(),
        widget=autocomplete.ModelSelect2(url='gari:county-autocomplete')
    )

    def clean(self):
        features = self.cleaned_data.get('features')
        print (features)

    class Meta:
        model = Vehicle
        fields = ('county', 'name', 'status', 'door', 'engine_size', 'gearbox', 'type', 'fuel_type', 'picture', 'year', 'price', 'make', 'model','mileage', 'color', 'tags', 'availability',
                                      'description', 'features', 'deal')


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ('first_name',
                  'last_name', 'email', 'phone_number', 'status', 'make', 'model', 'color', 'budget', 'description',
                  )


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('price', 'description')


class DealersForm(forms.ModelForm):
    county = autocomplete.Select2ListChoiceField(

        widget=autocomplete.ListSelect2(url='gari:county-autocomplete')
    )
    class Meta:
        model = Profile
        fields = ('county',)

