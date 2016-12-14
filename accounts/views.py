from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
import datetime
import stripe
import arrow
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import User

stripe.api_key = settings.STRIPE_SECRET

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=999,
                    currency="USD",
                    description=form.cleaned_data['email'],
                    card=form.cleaned_data['stripe_id'],


                )

            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined!")

            #if customer.paid:
            if customer:
                user = form.save()
                user.stripe_id = customer.id
                user.subscription_end = arrow.now().replace(weeks=+4).datetime
                user.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered" + str(customer))
                return redirect(reverse('profile'))
            else:
                messages.error(request, "unable to log you in at this time!")
        else:
            messages.error(request, "We were unable to take a payment with that card!")

    else:
        today = datetime.date.today()
        form = UserRegistrationForm()

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'register.html', args)

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'profile.html')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))
            if user is not None:
                subend = user.subscription_end
                datenow = arrow.now().datetime
                if datenow > subend:
                    cantloginmessage = "your subscription has expired, on" + str(subend)
                    messages.error(request, cantloginmessage)
                else:
                    auth.login(request, user)


                    login_message = "you have successfully logged in, your subscription will end on: " + str(subend)
                    messages.error(request, login_message)
                    return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email of password were not recognised")
    else:
        form = UserLoginForm()
    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request, "you have logged out")
    return redirect(reverse('index'))

@login_required(login_url='/accounts/login/')
def cancel_subscription(request):
   try:
       customer = stripe.Customer.retrieve(request.user.stripe_id)
       customer.cancel_subscription(at_period_end=True)
   except Exception, e:
       messages.error(request, e)
   return redirect('profile')
