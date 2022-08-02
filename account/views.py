from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.db.models import Q, F, When
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shared.decorators import ajax_required
from images.models import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import UserFilter, ProfileFilter
from django.template import Context
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Successful authenticated')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm
    return render(request, 'account/login.html', {'form': form})


def profile(request):
    proname = Profile.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'section': 'profile', 'proname': proname})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            #Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html')


    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
        else:
            messages.error(request, 'There was a problem when updating profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
GENDER_CHOICES = (('female', 'Female'),
                      ('male', 'Male'),
                      )
LOOKING_CHOICES = (('woman', 'Woman'),
                       ('man', 'Man'),
                       )


@login_required()
def member_list(request):
    male = User.objects.filter(profile__gender='male')
    page = request.GET.get('page', 1)
    paginator = Paginator(male, 5)

    try:
        male = paginator.page(page)
    except PageNotAnInteger:
        male = paginator.page(1)
    except EmptyPage:
        male = paginator.page(paginator.num_pages)

    female = User.objects.filter(profile__gender='female')
    page = request.GET.get('page', 1)
    paginator = Paginator(female, 4)

    try:
        female = paginator.page(page)
    except PageNotAnInteger:
        female = paginator.page(1)
    except EmptyPage:
        female = paginator.page(paginator.num_pages)
    context = {'male_list': male, 'female_list': female}
    return render(request,  'account/members.html', context=context)


def member_filter(request):
    f = UserFilter(request.GET, queryset=User.objects.all())
    return render(request, 'account/member_search.html', {'filter': f})


def member_results(request):
    f = UserFilter(request.GET, queryset=User.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(f.qs, 5)
    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        user = paginator.page(1)
    except EmptyPage:
        user = paginator.page(paginator.num_pages)

    return render(request, 'account/search.html', {'filter': f, 'user': user})


@login_required()
def member_detail(request, username):
    user = get_object_or_404(User, username=username
                               )
    photos = Image.objects.filter(user=user)
    return render(request, 'account/member_detail.html', {'section': 'members', 'user': user, 'photos': photos})






















