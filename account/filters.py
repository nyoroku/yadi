from django.contrib.auth.models import User
from .models import Profile
import django_filters
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField


GENDER_CHOICES = (('female', 'Female'),
                      ('male', 'Male'),
                      )

LOOKING_CHOICES = (('woman', 'Woman'),
                   ('man', 'Man'),
                   )


class UserFilter(django_filters.FilterSet):
    age = django_filters.NumberFilter(field_name='profile__age')
    age__gte = django_filters.NumberFilter(field_name='profile__age', lookup_expr='gte', label='Minimum Age')
    age__lte = django_filters.NumberFilter(field_name='profile__age', lookup_expr='lte', label='Maximum Age')
    gender = django_filters.ChoiceFilter(choices=GENDER_CHOICES, label='Looking for a', field_name='profile__gender')
    look_for = django_filters.ChoiceFilter(choices=LOOKING_CHOICES, label='Im a', field_name='profile__look_for')

    class Meta:
        model = User
        fields = ['profile']


class ProfileFilter(django_filters.FilterSet):
    country = CountryField('profile__country')

    class Meta:
        model = Profile
        fields = ['country']








