from django.http import HttpResponse
from .models import OrderInformation, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
import json
import time


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):

        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        if username != 'AnonUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_full_name = shipping_details.name
                profile.default_street_name_1 = shipping_details.address.line1
                profile.default_street_name_2 = shipping_details.address.line2
                profile.default_town_or_city = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_postal_code = shipping_details.address.postal_code
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = OrderInformation.objects.get(
                    full_name__iexact=shipping_details.name,
                    email_address__iexact=billing_details.email,
                    contact_number__iexact=shipping_details.phone,
                    street_name_1__iexact=shipping_details.address.line1,
                    street_name_2__iexact=shipping_details.address.line2,
                    town_or_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postal_code__iexact=shipping_details.address.postal_code,
                    grand_total=grand_total,
                    original_shopping_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except OrderInformation.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Success, Order already verifed in our databse',
                status=200)
        else:
            order = None
            try:
                order = OrderInformation.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email_address=billing_details.email,
                    contact_number=shipping_details.phone,
                    street_name_1=shipping_details.address.line1,
                    street_name_2=shipping_details.address.line2,
                    town_or_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postal_code=shipping_details.address.postal_code,
                    original_shopping_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
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
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | Error {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Success, Order created in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
