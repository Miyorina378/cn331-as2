from django.db import models

# Create your models here.
class Course(models.Model):
    courseCode = models.CharField(max_length=5)
    courseName = models.CharField(max_length=100)
    semester   = models.CharField(max_length=1)
    year = models.CharField(max_length=4)
    seat = models.CharField(max_length=4)