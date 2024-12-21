# teaching/admin.py

from django.contrib import admin
from .models import TeacherProfile, Student, LearningGoal

admin.site.register(TeacherProfile)
admin.site.register(Student)
admin.site.register(LearningGoal)
