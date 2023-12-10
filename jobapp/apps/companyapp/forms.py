from django import forms
from ..jobsapp.models import Company


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
        fields = ['company_name','description','city','country']
        
    #input fields
    company_name = forms.CharField(
        max_length=80,
        label= 'Company Name',
        widget= forms.TextInput(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary',
            'id':'company_name',
        })
    )
    
    description = forms.CharField(
        label= 'Company Description',
        widget= forms.Textarea(attrs={
            'class':'form-control rounded focus:ring-1 focus:ring-primary focus:border-primary resize-none',
            'id':'company_description',
            'row':5
        })
    )
    
    country = forms.CharField(
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
            'id':'company_city'
        })
    )
    
    