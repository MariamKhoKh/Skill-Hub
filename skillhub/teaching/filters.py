from django import forms
from django.db.models import Q
from .models import TeacherProfile


class TeacherFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control bg-dark text-light mb-3',
                'placeholder': 'Search by teacher name or skill...'
            }
        )
    )
    experience_range = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Experience'),
            ('1-3', '1-3 years'),
            ('4-6', '4-6 years'),
            ('7+', '7+ years')
        ],
        widget=forms.Select(
            attrs={'class': 'form-select bg-dark text-light mb-3'}
        )
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control bg-dark text-light mb-2',
                'placeholder': 'Min price'
            }
        )
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control bg-dark text-light mb-2',
                'placeholder': 'Max price'
            }
        )
    )
    min_rating = forms.FloatField(
        required=False,
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control bg-dark text-light mb-3',
                'placeholder': 'Minimum rating'
            }
        )
    )
    communication_methods = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('zoom', 'Zoom'),
            ('teams', 'Teams'),
            ('skype', 'Skype'),
            ('meet', 'Google Meet')
        ],
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
    )

    def filter_teachers(self, queryset):
        if not any(self.cleaned_data.values()):
            return queryset

        filters = Q()

        # Search query filter
        search_query = self.cleaned_data.get('search_query')
        if search_query:
            filters |= Q(user__username__icontains=search_query) | \
                      Q(user__first_name__icontains=search_query) | \
                      Q(user__last_name__icontains=search_query) | \
                      Q(skills__icontains=search_query) | \
                      Q(bio__icontains=search_query)

        # Experience range filter
        experience_range = self.cleaned_data.get('experience_range')
        if experience_range:
            if experience_range == '1-3':
                filters &= Q(experience_years__gte=1, experience_years__lte=3)
            elif experience_range == '4-6':
                filters &= Q(experience_years__gte=4, experience_years__lte=6)
            elif experience_range == '7+':
                filters &= Q(experience_years__gte=7)

        # Price range filter
        min_price = self.cleaned_data.get('min_price')
        if min_price is not None:
            filters &= Q(hourly_rate__gte=min_price)

        max_price = self.cleaned_data.get('max_price')
        if max_price is not None:
            filters &= Q(hourly_rate__lte=max_price)

        # Rating filter
        min_rating = self.cleaned_data.get('min_rating')
        if min_rating is not None:
            filters &= Q(rating__gte=min_rating)

        # Communication methods filter
        communication_methods = self.cleaned_data.get('communication_methods')
        if communication_methods:
            method_filters = Q()
            for method in communication_methods:
                method_filters |= Q(communication_methods__icontains=method)
            filters &= method_filters

        return queryset.filter(filters).distinct()