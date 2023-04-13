from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Customer


def home(request):
    customers = Customer.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("home")
        else:
            messages.warning(request, "Login failed")
            return redirect("home")
    else:
        return render(request, "home.html", {"customers": customers})


def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out")
    return render(request, "home.html", {})


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully registered")
            return render(request, "home.html", {})
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})
