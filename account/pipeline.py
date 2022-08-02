from .models import Profile


def save_profile(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)





