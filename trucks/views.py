from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, When, Value, Case, PositiveSmallIntegerField
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django_ajax.decorators import ajax
from .models import Truck, County, Feature, Image
from .forms import TruckForm, ImageFormSet
from gari.decorater import seller_required
from dal import autocomplete


class TruckListView(ListView):
    model = Truck
    template_name = 'truck/list.html'

    def get_queryset(self):
        qs = super(TruckListView, self).get_queryset()
        return qs.filter(seller=self.request.user)


class SellerMixin(object):
    def get_queryset(self):
        qs = super(SellerMixin, self).get_queryset()
        return qs.filter(seller=self.request.user)


class SellerEditMixin(object):
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(SellerEditMixin, form).form_valid(form)


class SellerTruckMixin(SellerMixin, LoginRequiredMixin):
    model = Truck

    success_url = reverse_lazy('trucks:my_list')




class SellerVehicleEditMixin(SellerTruckMixin, SellerEditMixin):


    template_name = 'truck/create.html'


class ManageTruckListView(SellerTruckMixin, ListView):
    template_name = 'truck/list.html'
    model = Truck
    context_object_name = 'trucks'
    paginate_by = 12
    queryset = Truck.objects.all()


@method_decorator([login_required, seller_required], name='dispatch')
class TruckCreateView(SuccessMessageMixin, SellerTruckMixin, CreateView, PermissionRequiredMixin):
    model = Truck
    form_class = TruckForm

    template_name = 'truck/create.html'
    success_message = '%(name)s Successfully Created.Please add at least eight pictures'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(TruckCreateView, self).form_valid(form)


@method_decorator([login_required, seller_required], name='dispatch')
class TruckUpdateView(SuccessMessageMixin, SellerTruckMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'truck/create.html'
    form_class = TruckForm
    success_url = reverse_lazy('trucks:my_list')
    success_message = '%(name)s Successfully Updated'


@method_decorator([login_required, seller_required], name='dispatch')
class TruckDeleteView(SuccessMessageMixin, SellerTruckMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'truck/delete.html'
    success_url = reverse_lazy('trucks:my_list')

    success_message = '%(name)s Successfully Deleted'


class CountyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):



        qs = County.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@method_decorator([login_required, seller_required], name='dispatch')
@method_decorator([login_required, ], name='dispatch')
class TruckImageUpdateView(TemplateResponseMixin, View):
    template_name = 'truck/formset.html'
    vehicle = None

    def get_formset(self, data=None):
        return ImageFormSet(instance=self.vehicle, data=data)

    def dispatch(self, request, pk):
        self.vehicle = get_object_or_404(Truck, id=pk, seller=request.user)
        return super(TruckImageUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'vehicle': self.vehicle, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = ImageFormSet(request.POST, request.FILES, instance=self.vehicle)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Image(s) Successfully  Updated')
            return HttpResponseRedirect(self.vehicle.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating image(s)')
        return self.render_to_response({'vehicle': self.vehicle, 'formset': formset})


def truck_detail(request,year,month,day, vehicle):
    vehicle = get_object_or_404(Truck, slug=vehicle)
    image = Image.objects.filter(vehicle=vehicle)[:6]
    features = Feature.objects.filter(truck=vehicle)
    truck_tag_ids = vehicle.tags.values_list('id', flat=True)
    similar_vehicles = Truck.objects.filter(Q(tags__in=truck_tag_ids) & Q(seller=vehicle.seller)).exclude(id=vehicle.id)
    similar_vehicles = similar_vehicles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:5]
    return render(request, 'truck/truck_detail.html', {'vehicle': vehicle, 'image': image,
                                                        'similar_vehicles': similar_vehicles, 'features': features})