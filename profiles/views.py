from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UsersProfileForm


def profiles(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    form = UsersProfileForm(instance=profile)
    order = profile.order.all()

    template = 'profiles/profiles.html'
    context = {
        'form': form,
        'order': order,
    }

    return render(request, template, context)
