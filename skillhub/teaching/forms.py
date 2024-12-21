from django import forms
from .models import TeacherProfile, TeacherSkill, Review, Student
from users.models import User


class TeacherProfileForm(forms.ModelForm):
    def clean_hourly_rate(self):
        rate = self.cleaned_data['hourly_rate']
        if rate < 0:
            raise forms.ValidationError("Hourly rate cannot be negative")
        return rate

    def clean_experience_years(self):
        years = self.cleaned_data['experience_years']
        if years < 0:
            raise forms.ValidationError("Experience years cannot be negative")
        return years

    class Meta:
        model = TeacherProfile
        fields = ['profile_picture', 'bio', 'skills', 'experience_years', 'hourly_rate', 'communication_methods']


class TeacherSkillForm(forms.ModelForm):
    class Meta:
        model = TeacherSkill
        fields = ['skill', 'proficiency_level']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class TeacherSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by teacher name or skill...'})
    )
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    min_rating = forms.FloatField(required=False)


class StudentUpdateForm(forms.ModelForm):
    achievements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comma-separated achievements'}),
        help_text="Comma-separated achievements (e.g., 'Math Olympiad Winner, Science Fair Participant')",
    )

    class Meta:
        model = Student
        fields = ['grade', 'track', 'achievements']

    def clean_achievements(self):
        data = self.cleaned_data.get('achievements', '')
        return ','.join([achievement.strip() for achievement in data.split(',') if achievement.strip()])


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
