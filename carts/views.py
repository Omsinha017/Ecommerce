from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from django.conf import settings
import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY" , 'sk_test_51HYzQfFTzilNLdNsovvquEhQaZ0QbIgZuRF6SO1uTleaFy2v7DGsao9jHNPj1HyuNaBwqdGh45nNQ2HNYRpjnoBp009wyDFnhb')
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", 'pk_test_51HYzQfFTzilNLdNs7pza8mQYY9mMbCH1esPm36N0qn7pliT0YfBPdSY2avDy6KVWl0NdfI8CIHPMqSTGwDGi71vg009Gd2nprg')

stripe.api_key = STRIPE_SECRET_KEY


def cart_detail_api_view(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id" : x.id,
        "name" : x.title, 
        "price": x.price,
        "url" : x.get_absolute_url(),
        } for x in cart_obj.products.all()]
    cart_data = {"products" : products,"subtotal" : cart_obj.subtotal,"total" : cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    return render(request,"carts/home.html",{"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product Gone ?")
            return redirect("cart:home")
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            added = False
            cart_obj.products.remove(product_obj)
        else:
            added = True
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
        
        if request.is_ajax:
            json_data = {
                "added" : added,
                "removed" : not added,
                "CartItemCount" : cart_obj.products.count(),
            }
            return JsonResponse(json_data,status=200)
    return redirect("cart:home")

def checkout_home(request):
    cart_obj,cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id",None)

    shipping_address_required = not cart_obj.is_digital

    shipping_address_id = request.session.get("shipping_address_id",None)

    billing_profile ,billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        
        if shipping_address_id :
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]

        if billing_address_id :
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]

        if shipping_address_id or billing_address_id :
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            did_charge,crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                return redirect("cart:checkout")
    context = {
        "object":order_obj,
        "billing_profile" : billing_profile,
        "login_form" : login_form,
        "guest_form" : guest_form,
        "address_form" : address_form,
        "billing_address_form" : billing_address_form,
        "address_qs" : address_qs,
        "has_card" : has_card,
        "publish_key" : STRIPE_PUB_KEY,
        "shipping_address_required" : shipping_address_required,
    }
    return render(request,"carts/checkout.html",context)


def checkout_done_view(request):
    return render(request,"carts/checkout-done.html",{})
