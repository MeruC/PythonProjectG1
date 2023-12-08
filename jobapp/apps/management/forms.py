# forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EditJobForm(forms.Form):
    job_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
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
                "class": "w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
            },
        ),
       
    )

    skills = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    def clean(self):
        cleaned_data = super().clean()
       
        return cleaned_data


class EditCompanyForm(forms.Form):
    company_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": " w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
                "rows": 5,
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    company_img = forms.ImageField(required=False,
        widget=forms.FileInput(
            
            attrs={
                "class": "hidden",
                'id': 'company_img',
             
            }
        ),
    )


    location = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full bg-[#F1F8F9] border-2 border-[#BABABA] px-2 py-1.5 mt-1 mb-1 rounded-md focus:outline-none focus:border-secondary",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    def clean(self):
        cleaned_data = super().clean()
       
        return cleaned_data
    
    
    
class EditCompanyImageForm(forms.Form):
   
    company_img = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "",
                'id': 'company_img',
                "required": "false",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
       
        return cleaned_data
