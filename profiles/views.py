from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UsersProfileForm


def profiles(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UsersProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Information has been successfull updated.')

    form = UsersProfileForm(instance=profile)
    order = profile.order.all()

    template = 'profiles/profiles.html'
    context = {
        'form': form,
        'order': order,
    }

    return render(request, template, context)
