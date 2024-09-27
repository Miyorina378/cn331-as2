from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.forms import RegisterForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse
from course.models import Course
from django.contrib import messages
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
def dashboard(request):
    enrolled_courses = Course.objects.filter(Users=request.user)
    return render(request, 'users/dashboard.html', {'enrolled_courses': enrolled_courses})

@login_required
def unenroll_from_course(request, course_code):

    course = get_object_or_404(Course, course_code=course_code)
    
    if request.user in course.Users.all():
        course.Users.remove(request.user)
        course.seat += 1
        if course.seat > 0 and course.seat < 2:
            course.seat_is_full = False
        course.save()
        messages.success(request, f"You have successfully withdraw from {course.course_name}.")
    else:
        messages.error(request, "You are not enrolled in this course.")

    return redirect('dashboard') 