from rest_framework import serializers
from .models import TeacherProfile


class TeacherProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = TeacherProfile
        fields = [
            'id',
            'name',
            'profile_picture',
            'bio',
            'skills',
            'hourly_rate',
            'communication_methods',
            'experience_years',
            'rating',
            'total_reviews',
            'join_date',
        ]
