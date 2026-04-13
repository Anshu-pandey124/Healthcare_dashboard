from django import forms
from .models import Doctor, Specialization

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'created_at']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'available_time_start': forms.TimeInput(attrs={'type': 'time'}),
            'available_time_end': forms.TimeInput(attrs={'type': 'time'}),
        }

class SpecializationForm(forms.ModelForm):
    doctors = forms.ModelMultipleChoiceField(
        queryset=Doctor.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        help_text="Select doctors to assign to this specialization"
    )
    class Meta:
        model = Specialization
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
