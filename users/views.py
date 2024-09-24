from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.forms import RegisterForm
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.urls import reverse
# Create your views here.

def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("courses"))
    else:
        form = RegisterForm()


    context = {"form": form}
    return render(request, "users/register.html", context)


def logout_user(request):
    logout(request)
    return redirect('courses')

@login_required
def dashboard(request: HttpRequest):
    return render(request, 'users/dashboard.html')