from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def index(request):
    return render(request, "index.html")


    

def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Registration was successful.")
            return redirect("login")

    else:
        form = UserCreationForm()
    return render(request, "registration/registration.html", {"form": form})


