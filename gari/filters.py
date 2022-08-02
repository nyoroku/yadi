from django.contrib.auth.models import User
from .models import Profile, Vehicle, Make, Model
from dal import autocomplete
import django_filters
from .models import County
from .forms import VehicleForm, DealersForm
from smart_selects.db_fields import ChainedForeignKey

STATUS = (('used', 'Used'),
          ('new', 'New'),
          ('import', 'Import')

          )

COLOR = (('red', 'Red'),
         ('blue', 'Blue'),
         ('black', 'Black')

         )

YEAR = ((2013, '2013'),
        (2014, '2014'),
        (2015,  '2015'),
        (2016, '2016'),
        (2017, '2017'),
        (2018,  '2018'),
        (2019, '2019'),
        (2020, '2020'),
        (2021,  '2021')

        )


class VehicleFilter(django_filters.FilterSet):
    make = django_filters.ModelChoiceFilter(queryset=Make.objects.all())
    model = django_filters.ModelChoiceFilter(queryset=Model.objects.all())
    mileage = django_filters.NumberFilter()
    mileage__lte = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte', label='Max Mileage')
    mileage__gte = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte', label='Min Mileage')
    price = django_filters.NumberFilter()
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    county = django_filters.ModelChoiceFilter(name='county',  queryset=County.objects.all(),
              widget=autocomplete.ModelSelect2(url='gari:county-autocomplete') )
    color = django_filters.ChoiceFilter(choices=COLOR, label='Color')
    year = django_filters.NumberFilter()
    year__lte = django_filters.ChoiceFilter(field_name='year', lookup_expr='lte', label='Year:To', choices=YEAR)
    year__gte = django_filters.ChoiceFilter(field_name='year', lookup_expr='gte', label='Year:From', choices=YEAR)

    class Meta:
        model = Vehicle
        widget = {'make': autocomplete.ModelSelect2(url='make-autocomplete', forward=['make'])}
        fields = ('status', 'county', 'model', 'mileage', 'color', 'price', 'year', 'status')


def get_choice_list():
    return [
            ['kirinyaga', 'Kirinyaga'],
            ['nairobi', 'Nairobi'],
            ['mombasa', 'Mombasa'],


        ]


class CountyFilter(django_filters.FilterSet):
    county = autocomplete.Select2ListChoiceField(choice_list=get_choice_list, widget=autocomplete.ListSelect2(url='gari:county-autocomplete'))


    class Meta:
        model = Profile
        fields = ['county', ]

