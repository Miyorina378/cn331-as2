from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_code = models.CharField(max_length=5)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField(null=True)
    semester   = models.CharField(max_length=1)
    year = models.CharField(max_length=4)
    seat = models.IntegerField() 
    seat_is_full = models.BooleanField(null=True)
    users = models.ManyToManyField(User, related_name='courses', blank=True)

    def __str__(self):
      return self.course_code + ' | ' + self.course_name
    
    def enroll_student(self, user):
       if self.seat > 0 and self.seat_is_full == False:
          self.users.add(user)
          self.seat -= 1
          if self.seat == 0:
             self.seat_is_full = True
          self.save()
          return True
       else:
          return False
    
    def unenroll_student(self, user):
        if user  in self.Users.all():
            self.users.remove(user)
            self.seat += 1
            if self.seat > 0:
                self.seat_is_full = False 
            self.save()
            return True
        return False
    
Course.Users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses", blank=True)