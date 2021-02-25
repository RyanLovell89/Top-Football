from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UsersProfileForm
from checkout.models import OrderInformation


def profiles(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UsersProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been successfull updated.')
        else:
            messages.error(request, 'Error! Your information was not updated, please check the form')
    else:
        form = UsersProfileForm(instance=profile)
    order = profile.order.all()

    template = 'profiles/profiles.html'
    context = {
        'form': form,
        'order': order,
    }

    return render(request, template, context)


def order_number_history(request, order_number):
    order = get_object_or_404(OrderInformation, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
