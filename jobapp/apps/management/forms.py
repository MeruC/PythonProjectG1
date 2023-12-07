# forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EditJobForm(forms.Form):
    job_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-gray-300 p-2 rounded-md focus:outline-none focus:border-secondary",
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-gray-300 p-2 rounded-md focus:outline-none focus:border-secondary",
                "rows": 5,
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    type_choices = [("parttime", "Part Time"), ("fulltime", "Full Time")]
    type = forms.ChoiceField(
        choices=type_choices,
        widget=forms.Select(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-gray-300 p-2 rounded-md focus:outline-none focus:border-secondary",
            },
        ),
       
    )

    skills = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-gray-300 p-2 rounded-md focus:outline-none focus:border-secondary",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    def clean(self):
        cleaned_data = super().clean()
       
        return cleaned_data
