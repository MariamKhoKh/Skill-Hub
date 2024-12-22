from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    communication_methods = models.TextField(help_text="Comma-separated list of skills")
    experience_years = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.PositiveIntegerField(default=0)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class TeacherSkill(models.Model):
    teacher_profile = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ])

    class Meta:
        unique_together = ('teacher_profile', 'skill')

    def __str__(self):
        return f"{self.teacher_profile.user.username} - {self.skill.name}"


class Review(models.Model):
    teacher_profile = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher_profile', 'student')

    def __str__(self):
        return f"Review for {self.teacher_profile.user.username} by {self.student.username}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    track = models.CharField(max_length=50)
    join_date = models.DateField(auto_now_add=True)
    total_hours = models.PositiveIntegerField(default=0)
    subject_count = models.PositiveIntegerField(default=0)
    achievements = models.TextField(help_text="Comma-separated achievements")


def __str__(self):
    return f"{self.user.username}'s Student Profile"


def achievements_list(self):
    return [a.strip() for a in self.achievements.split(',')] if self.achievements else []


class LearningGoal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=255)
    progress = models.PositiveIntegerField(default=0)





