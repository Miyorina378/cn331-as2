from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def courses(request: HttpRequest):
    return render(request, 'course/courses.html')

def about(request: HttpRequest):
    return render(request, 'course/about.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "course/login.html",{
                "message": "Invalid credentials"
            })
    return render(request, 'course/login.html')

def logout_view(request):
    logout(request)
    return render(request, "course/login.html", {"message":  "logged out" })