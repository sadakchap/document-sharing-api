from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.

def register(request):
    _next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        pwrd = form.cleaned_data.get('password2')
        user = form.save(commit=False)
        user.email = email
        user.set_password(pwrd)
        user.save()
        new_obj = authenticate(username=email, password=pwrd) 
        login(request, new_obj)
        if _next:
            return redirect(_next)
        return redirect('/')
    return render(request, 'registration/register.html', {'form':form})

def login_view(request):
    _next = request.GET.get('next')
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