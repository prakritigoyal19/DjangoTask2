from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login
# Create your views here.


def homepage(request):
    return render(request, 'ne/homepage.html')


def register(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/')

    else:
        form = forms.UserForm()

    context = {'form': form}
    return render(request, 'registration/registration.html', context)
