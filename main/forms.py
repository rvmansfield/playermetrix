from django import forms
from .models import PlayerMetric, PlayerProfile
from allauth.account.forms import SignupForm

class PlayerMetricForm(forms.ModelForm):
    class Meta:
        model = PlayerMetric
        fields = ['metricType', 'metric', 'playerAge']
        widgets = {
            'metricType': forms.Select(attrs={'class': 'form-control'}),
            'metric': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter metric value (e.g., 85.5)',
                'step': '0.01',
                'min': '0',
                'onchange': 'validateNumeric(this)'
            }),
            'playerAge': forms.Select(attrs={'class': 'form-control'}),
        }


class CaptureForm(forms.Form):
    """Form for capturing multiple metrics at once"""
    
    # Common fields for all metrics
    playerAge = forms.IntegerField(
        widget=forms.Select(choices=[("", "---------")] + [(i, str(i)) for i in range(12, 21)], attrs={'class': 'form-control'}),
        label='Player Age',
        help_text='Select player age'
    )
    dateCaptured = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date Captured',
        required=True,
        help_text='When were these metrics recorded?'
    )
    capturedBy = forms.ChoiceField(
        choices=[
            ("", "---------"),
            ('Perfect Game', 'Perfect Game'),
            ('Player Metrix', 'Player Metrix'),
            ('Prep Baseball', 'Prep Baseball'),
            ('Self Captured', 'Self Captured'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Captured By',
        required=False,
        help_text='Who captured these metrics?'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about these metrics...', 'maxlength': '500'}),
        label='Notes',
        required=False,
        max_length=500,
        help_text='Optional notes about these metrics'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add metric fields for each metric type
        for metric_type, display_name in PlayerMetric.METRIC_TYPE_CHOICES:
            field_name = f'metric_{metric_type}'
            self.fields[field_name] = forms.DecimalField(
                widget=forms.TextInput(attrs={
                    'class': 'form-control metric-input',
                    'placeholder': f'Enter {display_name.lower()}',
                    'pattern': r'^\d+(\.\d{1,2})?$',
                    'title': 'Enter a number with up to 2 decimal places'
                }),
                label=display_name,
                required=False,
                max_digits=8,
                decimal_places=2
            )


class PlayerSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        return user


class PlayerProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    positions = forms.MultipleChoiceField(
        choices=PlayerProfile.POSITION_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '7'})
    )

    class Meta:
        model = PlayerProfile
        fields = ['firstName', 'lastName', 'team', 'school', 'graduation_year', 'city', 'state', 'throws', 'hits', 'picture', 'bio']
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'team': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'throws': forms.Select(attrs={'class': 'form-control'}),
            'hits': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'graduation_year': 'Graduation Year',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.positions:
            self.fields['positions'].initial = self.instance.get_positions_list()

    def save(self, commit=True):
        profile = super().save(commit=False)
        positions_data = self.cleaned_data.get('positions', [])
        profile.positions = ','.join(positions_data) if positions_data else None
        if commit:
            profile.save()
        return profile
