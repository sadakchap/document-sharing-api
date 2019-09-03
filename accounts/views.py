from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm

# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        pswrd = form.cleaned_data.get('password')
        if email and pswrd:
            user = authenticate(username=email, password=pswrd)
            if user:
                login(request, user)
                return redirect('/')
    return render(request, "registration/login.html", {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')