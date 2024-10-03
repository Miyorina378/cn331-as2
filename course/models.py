from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
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
    Users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CourseEnrollment', related_name='enrolled_courses', blank=True)
    
    def __str__(self):
      return self.course_code + ' | ' + self.course_name
    
    def enroll_student(self, user):
        if CourseEnrollment.objects.filter(user=user, course=self).exists():
            return False
        if self.seat > 0 and not self.seat_is_full:
            CourseEnrollment.objects.create(user=user, course=self)
            self.seat -= 1
            if self.seat == 0: 
                self.seat_is_full = True
            self.save()
            return True
        return False
    
class CourseEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enroll_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'course')  
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_code}"

@receiver(post_delete, sender=CourseEnrollment)
def increase_seat_on_unenroll(sender, instance, **kwargs):
    course = instance.course
    course.seat += 1
    if course.seat > 0:
        course.seat_is_full = False
    course.save()

    
