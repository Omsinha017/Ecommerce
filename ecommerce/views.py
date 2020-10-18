from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .forms import ContactForm
from django.contrib.auth import authenticate,login,get_user_model


def home_page(request):
    context = {
        "title" : "Hello There",
        "content" : " OK OK"
     }
    if request.user.is_authenticated:
        context["premium"] = "yeahh working"
    return render(request,'home_page.html',context)


def Contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Welcome to contact Form",
        "form" : contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax:
            return JsonResponse({"message" : "Thank You"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax:
            return HttpResponse(errors,status = 400, content_type='application/json')


    return render(request,"contact/contact_fom.html",context)

