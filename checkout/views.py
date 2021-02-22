from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderingForm
# Create your views here.


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "The bag is empty at the moment")
        return redirect(reverse('products'))

    order_form = OrderingForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51ICNUDAKqzi40Ijpw0YaQM3BtxeeoOXEYTSYMKJelAnxz4MoqNXMXybJ88mw79oDR35eNl9llBXLddg2VN5zZYSd00Tza8Oo0i',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)
