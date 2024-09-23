from django.db import models

# Create your models here.
class Course(models.Model):
    course_code = models.CharField(max_length=5)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField(null=True)
    semester   = models.CharField(max_length=1)
    year = models.CharField(max_length=4)
    seat = models.IntegerField() 
    seat_is_full = models.BooleanField(null=True)

    def __str__(self):
      return self.course_code + ' | ' + self.course_name