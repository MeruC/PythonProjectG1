from django import forms
from django.utils import timezone
from ..jobsapp.models import Job
from datetime import datetime
from ckeditor.widgets import CKEditorWidget
from ..jobsapp.models import Company
from django_countries import countries

class CompanyLogoForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['logo']
        
    logo = forms.ImageField(
        label='',
        widget=forms.ClearableFileInput(attrs={'id': 'file_input'})
        )
    
    
class CompanyCoverForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['cover_photo']
        
    cover_photo = forms.ImageField(
        label='',
        widget=forms.ClearableFileInput(attrs={'id': 'file_input_cover'})
        )
    
    
class CompanyDataForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name','email_address','description','city','country']
        
    #input fields
    company_name = forms.CharField(
        max_length=80,
        label= 'Company Name',
        widget= forms.TextInput(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary',
            'id':'company_name',
            'placeholder':'Enter Company Name'
        })
    )
    
    email_address = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary',
            'id':'email_address',
            'placeholder':'Enter Company Email '
        })
    )
    
    description = forms.CharField(
        label= 'Company Description',
        widget= forms.Textarea(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary resize-none',
            'id':'company_description',
            'row':5,
            'placeholder':'Enter Company Description'
        })
    )
    
    country = forms.ChoiceField(
        choices=[('', 'Select your Country')] + list(countries),  #add default option
        widget=forms.Select(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary',
            'id':'company_country',
        })
    )
    
    city = forms.CharField(
        max_length=95,
        label='City',
        widget=forms.TextInput(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary',
            'id':'company_city',
            'placeholder':'Enter City'
        })
    )
    

class JobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ["job_title", "description", "type", "skills", "min_salary", "max_salary", "status", "date_posted"]
        
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
        widget=CKEditorWidget(attrs={
            "class": "block border w-full rounded-md p-2 border-gray-400 outline-none",
            "autocomplete": "off",
            "required": "true",
        }),
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

    min_salary = forms.IntegerField(
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
    
    max_salary = forms.IntegerField(
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
    
    date_posted = forms.DateTimeField(
        label="Date Posted",
        widget=forms.DateTimeInput(
            attrs={
                "autocomplete": "off",
                # "required": "true",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the default value for date_created
        self.fields['date_posted'].initial = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get("min_salary")
        max_salary = cleaned_data.get("max_salary")
        date_posted = cleaned_data.get("date_posted")
        
        if min_salary > max_salary:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")
        
        if date_posted > datetime.now(timezone.utc):
            raise forms.ValidationError("Date posted cannot be greater than today.")
        
        return cleaned_data
    
    def save(self, commit=True):
        job = super().save(commit=False)
        job.save()
        return job
    
        
