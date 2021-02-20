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
    }

    return render(request, template, context)
