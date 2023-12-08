from django import forms
from django.utils import timezone
from .models import Job
from datetime import datetime

class JobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ["job_title", "description", "type", "skills", "minimum_salary", "maximum_salary", "status", "date_created"]
        
    job_title = forms.CharField(
        label="Job Title",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
                "placeholder": "Marketing Specialist",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    
    description = forms.CharField(
        label="Job Description",
        widget=forms.Textarea(
            attrs={
                "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
                "placeholder": "We are seeking a highly motivated and creative Marketing Specialist to join our dynamic team. The ideal candidate will play a key role in developing and implementing effective marketing strategies to promote our products/services. This position requires a combination of strategic thinking, strong analytical skills, and hands-on execution of marketing initiatives across various channels.",
                "autocomplete": "off",
                "required": "true",
                "rows":"10",
                "style":"resize:none",
            }
        ),
    )
    
    type = forms.TypedChoiceField(
        label="Job Type",
        choices=Job.TYPE_CHOICES,
        coerce=lambda x: x,
        empty_value=None,
        widget=forms.Select(
            attrs={
                "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
                "autocomplete": "off",
            }
        )
    )
    
    skills = forms.CharField(
        label="Skills",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
                "placeholder": "Strategic Thinking, Adaptability, Data Analysis",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )

    minimum_salary = forms.DecimalField(
        label="Minimum Salary",
        widget=forms.NumberInput(
            attrs={
                "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
                "placeholder": "10000",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    
    maximum_salary = forms.DecimalField(
        label="Maximum Salary",
        widget=forms.NumberInput(
            attrs={
                "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
                "placeholder": "20000",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    
    status = forms.TypedChoiceField(
        label="Job Status",
        choices=Job.STATUS_CHOICES,
        coerce=lambda x: x,
        empty_value=None,
        widget=forms.Select(
            attrs={
                "class": "block border rounded-md p-2 border-gray-400 outline-none w-full",
                "autocomplete": "off",
            }
        )
    )
    
    date_created = forms.DateTimeField(
        label="Date Created",
        widget=forms.DateTimeInput(
            attrs={
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the default value for date_created
        self.fields['date_created'].initial = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
