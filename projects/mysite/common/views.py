from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from common.forms import UserForm


def logout_view(req):
    logout(req)
    return redirect("index")


def signup(req):
    if req.method == "POST":
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect("index")
    else:
        form = UserForm()
    return render(req, "common/signup.html", {"form": form})
