from django import forms
from .models import Course

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name']