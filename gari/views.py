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
from .models import Vehicle, Image, User, Profile, Private, Make, Model,County, Feature, Service,Quote, Offer, Blog,Type
from .forms import ImageFormSet, DealerSignUPForm, PrivateSignUPForm, UserEditForm, ProfileEditForm, PrivateEditForm, VehicleForm, QuoteForm, OfferForm, DealersForm
from .decorater import seller_required
from dal import autocomplete
from .filters import VehicleFilter, CountyFilter
from datetime import datetime, date, timedelta


class VehicleListView(ListView):
    model = Vehicle
    template_name = 'gari/list.html'

    def get_queryset(self):
        qs = super(VehicleListView, self).get_queryset()
        return qs.filter(seller=self.request.user)


class SellerMixin(object):
    def get_queryset(self):
        qs = super(SellerMixin, self).get_queryset()
        return qs.filter(seller=self.request.user)


class SellerEditMixin(object):
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(SellerEditMixin, form).form_valid(form)


class SellerVehicleMixin(SellerMixin, LoginRequiredMixin):
    model = Vehicle

    success_url = reverse_lazy('gari:my_list')


class SellerVehicleEditMixin(SellerVehicleMixin, SellerEditMixin):

    template_name = 'gari/create.html'


class ManageVehicleListView(SellerVehicleMixin, ListView):
    template_name = 'gari/list.html'
    model = Vehicle
    context_object_name = 'vehicles'
    paginate_by = 12
    queryset = Vehicle.objects.all()


@method_decorator([login_required, seller_required], name='dispatch')
class VehicleCreateView(SuccessMessageMixin, SellerVehicleMixin, CreateView, PermissionRequiredMixin):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'gari/create.html'
    success_message = '%(name)s Successfully Created.Please add at least eight pictures'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(VehicleCreateView, self).form_valid(form)


@method_decorator([login_required, seller_required], name='dispatch')
class VehicleUpdateView(SuccessMessageMixin, SellerVehicleMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'gari/create.html'
    form_class = VehicleForm
    success_url = reverse_lazy('gari:my_list')
    success_message = '%(name)s Successfully Updated'


@method_decorator([login_required, seller_required], name='dispatch')
class VehicleDeleteView(SuccessMessageMixin, SellerVehicleMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'gari/delete.html'
    success_url = reverse_lazy('gari:my_list')

    success_message = '%(name)s Successfully Deleted'


@method_decorator([login_required, seller_required], name='dispatch')
@method_decorator([login_required, ], name='dispatch')
class VehicleImageUpdateView(TemplateResponseMixin, View):
    template_name = 'gari/formset.html'
    vehicle = None

    def get_formset(self, data=None):
        return ImageFormSet(instance=self.vehicle, data=data)

    def dispatch(self, request, pk):
        self.vehicle = get_object_or_404(Vehicle, id=pk, seller=request.user)
        return super(VehicleImageUpdateView, self).dispatch(request, pk)

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


def vehicle_detail(request,year,month,day, vehicle):
    vehicle = get_object_or_404(Vehicle, slug=vehicle)
    image = Image.objects.filter(vehicle=vehicle)[:6]
    features = Feature.objects.filter(vehicle=vehicle)
    vehicle_tag_ids = vehicle.tags.values_list('id', flat=True)
    similar_vehicles = Vehicle.objects.filter(Q(tags__in=vehicle_tag_ids) & Q(seller=vehicle.seller)).exclude(id=vehicle.id)
    similar_vehicles = similar_vehicles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:5]
    return render(request, 'gari/vehicle_detail.html', {'vehicle': vehicle, 'image': image,
                                                        'similar_vehicles': similar_vehicles, 'features': features})


class DealerSignUpView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'gari/registration.html'
    form_class = DealerSignUPForm
    success_url = reverse_lazy('gari:my_list')
    success_message = 'Thank You %(username)s for joining our team.Please complete your profile detail'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'profile'
        return super(DealerSignUpView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.save()
        result = super(DealerSignUpView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'], )

        login(self.request, user)

        return result


class PrivateSignUpView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'gari/register.html'
    form_class = PrivateSignUPForm
    success_url = reverse_lazy('gari:my_list')
    success_message = 'Thank You %(username)s for joining our team.Please complete your profile detail'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'profile'
        return super(PrivateSignUpView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.save()
        result = super(PrivateSignUpView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'], )

        login(self.request, user)

        return result


def common_view(request):
    user = request.user
    if user.is_finder:
        return redirect('index')

    else:
        return redirect('gari:my_list')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('gari:profile')
        else:
            messages.error(request, 'There was a problem when updating profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'gari/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


def profile(request):
    proname = Profile.objects.filter(user=request.user)
    return render(request, 'gari/profile.html', {'section': 'profile', 'proname': proname})


def my_profile(request):
    proname = Private.objects.filter(user=request.user)
    return render(request, 'gari/my_profile.html', {'section': 'profile', 'proname': proname})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        profile_form = PrivateEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('gari:my_profile')
        else:
            messages.error(request, 'There was a problem when updating profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = PrivateEditForm(instance=request.user.profile)
    return render(request, 'gari/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


def load_models(request):
    make_id = request.GET.get('make')
    models = Model.objects.filter(make_id=make_id).order_by('name')
    return render(request, 'gari/models_dropdown.html', {'models': models})


class CountyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = County.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class ModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Make.objects.all()
        make = self.forwarded.get('make', None)
        if make:
            qs = qs.filter(make=make)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DealerCountyAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return [
            ['kirinyaga', 'Kirinyaga'],
            ['nairobi', 'Nairobi'],
            ['mombasa', 'Mombasa'],


        ]


def countyfilter(request):
    f = CountyFilter(request.GET, queryset=Profile.objects.all())
    dealer = f.qs
    total_dealers = dealer.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(dealer, 1)
    try:
        dealer = paginator.page(page)
    except PageNotAnInteger:
        dealer = paginator.page(1)
    except EmptyPage:
        dealer = paginator.page(paginator.num_pages)

    return render(request, 'gari/county_dealers.html',
                  {'filter': f, 'dealer': dealer, 'total_dealers': total_dealers,
                   })





def gari_pad(request):
    f = VehicleFilter(request.GET, queryset=Vehicle.objects.all())
    form = VehicleForm
    return render(request, 'gari/index.html', {'filter': f, 'form': form})


def gari_results(request, tag_slug=None):
    f = VehicleFilter(request.GET, queryset=Vehicle.objects.all())
    g = VehicleFilter(request.GET, queryset=Vehicle.objects.filter(sponsored=True))
    order = request.GET.get('order', 'price')
    vehicle = f.qs
    sponsored = g.qs
    f = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        f = vehicle.filter(tags__in=[tag])

    total_vehicles = vehicle.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(f, 24)
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)

    return render(request, 'gari/used_results.html', {'filter': f, 'vehicle': vehicle, 'total_vehicles': total_vehicles,
                                                      'tag': tag, 'order': order, 'g': g , 'sponsored': sponsored})


def garipad(request):
    f = VehicleFilter(request.GET, queryset=Vehicle.objects.filter(status='new'))
    return render(request, 'gari/used_search.html', {'filter': f})


def all_vehicles(request, tag_slug=None):
    vehicle = Vehicle.objects.all().order_by('sponsored')
    sponsored = Vehicle.objects.filter(sponsored=True)
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
        sponsored = vehicle.filter(Q(tags__in=[tag]) & Q(sponsored=True))
    total_vehicle = vehicle.count()
    paginator = Paginator(vehicle, 24)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_vehicles.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag, 'total_vehicle': total_vehicle,
                                                      'sponsored': sponsored})


def all_dealers(request):
    f = CountyFilter(request.GET, queryset=Profile.objects.all())

    dealer = Profile.objects.all()
    order = request.GET.get('company')
    dealer = dealer.order_by()
    total_dealer = dealer.count()
    paginator = Paginator(dealer, 5)
    page = request.GET.get('page')
    try:
        dealer = paginator.page(page)
    except PageNotAnInteger:
        dealer = paginator.page(1)
    except EmptyPage:
        dealer = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_dealer.html', {'order': order, 'dealer': dealer, 'page': page,
                                                    'total_dealer': total_dealer, 'filter': f })


def dealer_detail(request,year,month,day, profile):
    profile = get_object_or_404(Profile, slug=profile)
    service = Service.objects.filter(profile=profile)
    used = Vehicle.objects.filter(Q(status='used') & Q(seller=profile.user))
    new = Vehicle.objects.filter(Q(status='new') & Q(seller=profile.user))
    imports = Vehicle.objects.filter(Q(status='import') & Q(seller=profile.user))
    return render(request, 'gari/dealer_detail.html', {'used': used, 'profile': profile, 'new': new,
                                                       'imports': imports, 'service': service})


def dealer_used(request, pk, tag_slug=None, ):
    profile = Profile.objects.get(pk=pk)
    vehicle = Vehicle.objects.filter(Q(status='used') & Q(seller=profile.user))
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
    total_vehicle = vehicle.count()
    paginator = Paginator(vehicle, 5)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_vehicles.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag,
                                                      'total_vehicle': total_vehicle})


def dealer_new(request, pk, tag_slug=None, ):
    profile = Profile.objects.get(pk=pk)
    vehicle = Vehicle.objects.filter(Q(status='new') & Q(seller=profile.user))
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
    total_vehicle = vehicle.count()
    paginator = Paginator(vehicle, 5)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_vehicles.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag,
                                                      'total_vehicle': total_vehicle})


def dealer_import(request, pk, tag_slug=None, ):
    profile = Profile.objects.get(pk=pk)
    vehicle = Vehicle.objects.filter(Q(status='import') & Q(seller=profile.user))
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
    total_vehicle = vehicle.count()
    paginator = Paginator(vehicle, 12)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_vehicles.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag,

                                                      'total_vehicle': total_vehicle})


def create_quote(request):
    if request.method == 'POST':
        form = QuoteForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            return render(request,
                          'gari/quoted.html',
                          {'quote': quote})
        else:
            messages.error(request, 'Something Went Wrong')
    else:
        form = QuoteForm()
    return render(request, 'gari/quote.html', {'form': form})


def all_quotes(request):
    quote = Quote.objects.all()
    order = request.GET.get('make', 'budget')
    quote = quote.order_by(order)

    total_quotes = quote.count()
    paginator = Paginator(quote, 12)
    page = request.GET.get('page')
    try:
        quote = paginator.page(page)
    except PageNotAnInteger:
        quote = paginator.page(1)
    except EmptyPage:
        quote = paginator.page(paginator.num_pages)
    return render(request, 'gari/total_quotes.html', {'order': order, 'quote': quote, 'page': page, 'total_quotes': total_quotes})


def my_quotes(request):
    quote = Quote.objects.filter(client=request.user)
    order = request.GET.get('make', 'budget')
    quote = quote.order_by(order)

    total_quotes = quote.count()
    paginator = Paginator(quote, 10)
    page = request.GET.get('page')
    try:
        quote = paginator.page(page)
    except PageNotAnInteger:
        quote = paginator.page(1)
    except EmptyPage:
        quote = paginator.page(paginator.num_pages)
    return render(request, 'gari/my_quotes.html', {'order': order, 'quote': quote, 'page': page, 'total_quotes': total_quotes})


def quote_detail(request,year,month,day, quote):
    quotes = get_object_or_404(Quote, slug=quote)

    return render(request, 'gari/dealer_detail.html', {'quotes': quotes})


def make_offer(request, quote_id):

    quote = get_object_or_404(Quote, pk=quote_id)
    if request.method == 'POST':
        form = OfferForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.quote = quote
            new_form.profile = request.user
            new_form.save()
            messages.success(request, 'Your offer has been sent')

        else:
            messages.error(request, 'There has been an error sending your message')
    else:
        form = OfferForm()
    return render(request, 'gari/offer.html', {'form': form, 'quote': quote})


def all_makes(request):
    make = Make.objects.all()
    order = request.GET.get('name')
    make = make.order_by()
    total_makes = make.count()
    paginator = Paginator(make, 24)
    page = request.GET.get('page')
    try:
        make = paginator.page(page)
    except PageNotAnInteger:
        make = paginator.page(1)
    except EmptyPage:
        make = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_makes.html', {'order': order, 'make': make, 'page': page,  'total_makes': total_makes })


def make_detail(request,year,month,day, make):
    make = get_object_or_404(Make, slug=make)
    models = Model.objects.filter(make=make)
    deals = Vehicle.objects.filter(Q(status='new') & Q(make=make) & Q(deal=True))
    dealers = Profile.objects.filter(makes=make)
    news = Blog.objects.filter(make=make)
    return render(request, 'gari/make_detail.html', {'make': make, 'models': models, 'deals': deals,
                                                     'dealers': dealers, 'news': news})


def allnews(request, tag_slug=None):
    news = Blog.objects.order_by('-created')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_news.html', {'news': news, 'page': page, 'tag' : tag})


def latest_detail(request, year, month, day, new):
    new = get_object_or_404(Blog, slug=new)
    new_tag_ids = new.tags.values_list('id', flat=True)
    similar_news = Blog.objects.filter(tags__in=new_tag_ids).exclude(id=new.id)
    similar_news = similar_news.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:3]
    return render(request, 'gari/news_detail.html', {'new': new, 'similar_news': similar_news})


def all_type(request):
    type = Type.objects.all()
    order = request.GET.get('name')
    type = type.order_by()
    total_types = type.count()
    paginator = Paginator(type, 5)
    page = request.GET.get('page')
    try:
        type = paginator.page(page)
    except PageNotAnInteger:
        type = paginator.page(1)
    except EmptyPage:
        type = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_types.html', {'order': order, 'type': type, 'page': page,  'total_types': total_types})


def type_detail(request,year,month,day, type, tag_slug=None, ):
    type = get_object_or_404(Type, slug=type)
    vehicle = Vehicle.objects.filter(type=type)
    sponsored = Vehicle.objects.filter(Q(type=type) & Q(sponsored=True))
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
    total_vehicle = vehicle.count()
    paginator = Paginator(vehicle, 5)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/type.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag,
                                                      'total_vehicle': total_vehicle, 'type': type, 'sponsored': sponsored})


def model_detail(request,year,month,day, model, tag_slug=None, ):
    model = get_object_or_404(Model, slug=model)
    vehicle = Vehicle.objects.filter(model=model)
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
    total_vehicle = vehicle.count()
    paginator = Paginator(vehicle, 24)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_models.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag,
                                                      'total_vehicle': total_vehicle, 'model': model})


def all_deals(request, tag_slug=None):

    now = datetime.now().date()
    vehicle = Vehicle.objects.all()
    sponsored = Vehicle.objects.filter(sponsored=True)
    order = request.GET.get('order', 'price')
    vehicle = vehicle.order_by(order)
    deals = vehicle.filter(Q(deal=True) & Q(deal_deadline__gte=now))

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        vehicle = vehicle.filter(tags__in=[tag])
        sponsored = vehicle.filter(Q(tags__in=[tag]) & Q(sponsored=True))
    total_vehicle = deals.count()
    paginator = Paginator(vehicle, 24)
    page = request.GET.get('page')
    try:
        vehicle = paginator.page(page)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)
    return render(request, 'gari/all_deals.html', {'order': order, 'vehicle': vehicle, 'page': page, 'tag': tag, 'total_vehicle': total_vehicle,
                                                      'sponsored': sponsored, 'deals': deals})