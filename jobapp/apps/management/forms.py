# forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EditJobForm(forms.Form):
    job_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
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
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
            },
        ),
       
    )

    skills = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
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
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
                "rows": 5,
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )

    logo = forms.ImageField(required=False,
        widget=forms.FileInput(
            
            attrs={
                "class": "hidden",
                'id': 'logo',
             
            }
        ),
    )


    country = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
                "autocomplete": "off",
                "required": "true",
            },
        ),
        
    )
    
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded focus:ring-1 focus:ring-primary focus:border-primary",
                "autocomplete": "off",
                "required": "true",
            },
        ),
    )

    
    def clean(self):
        cleaned_data = super().clean()
       
        return cleaned_data
    
    
    
class EditCompanyImageForm(forms.Form):
   
    logo = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "",
                'id': 'logo',
                "required": "false",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
       
        return cleaned_data
