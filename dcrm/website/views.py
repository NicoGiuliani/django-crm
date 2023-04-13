from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
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


def customer_record(request, pk):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(id=pk)
            return render(request, "customer.html", {"customer": customer})
        except ObjectDoesNotExist:
            messages.warning(request, "Customer record not found")
            return redirect("home")
    else:
        messages.warning(request, "You must be logged in to view that page")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(id=pk)
            customer.delete()
            messages.success(request, "Customer deleted")
            return redirect("home")
        except ObjectDoesNotExist:
            messages.warning(request, "Customer record not found")
            return redirect("home")
    else:
        messages.warning(request, "You must be logged in to delete user records")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "New customer has been added")
                return redirect("home")

        return render(request, "new_customer.html", {"form": form})
    else:
        messages.info(request, "You must be logged in to add new customers")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer has been updated")
            return redirect("home")
        else:
            return render(request, "update_customer.html", {"form": form})
    else:
        messages.info(request, "You must be logged in to update customers")
        return redirect("home")
