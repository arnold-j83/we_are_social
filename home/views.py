from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.forms import UserRegistrationForm
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf

def get_index(request):
    return render(request, 'index.html')

