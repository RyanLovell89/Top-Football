from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderingForm
from bag.contexts import bag_contents
from products.models import Product
from .models import OrderInformation, OrderLineItem
import json
import stripe
# Create your views here.


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save-info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment has has not been \
            processed, Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email_address': request.POST['email_address'],
            'contact_number': request.POST['contact_number'],
            'street_name_1': request.POST['street_name_1'],
            'street_name_2': request.POST['street_name_2'],
            'town_or_city': request.POST['town_or_city'],
            'postal_code': request.POST['postal_code'],
            'county': request.POST['county'],
        }
        order_form = OrderingForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['item_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in the bag was not found in database."
                        "Please contact us for help"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_successful', args=[order.order_number]))
        else:
            messages.error(request, 'There is an error with the your form. \
                Please check you have enter the correct information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "The bag is empty at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderingForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_successful(request, order_number):

    save_info = request.session.get('save_info')
    order = get_object_or_404(OrderInformation, order_number=order_number)
    messages.success(request, f'Your order has gone through successfully \
        Your order number is {order.order_number} \
            And a confirmation email has been sent to {order.email_address}')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_successful.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
