# teaching/admin.py

from django.contrib import admin
from .models import TeacherProfile, Student

admin.site.register(TeacherProfile)
admin.site.register(Student)

