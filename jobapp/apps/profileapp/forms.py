from django import forms
from apps.accountapp.models import User
from apps.jobsapp.models import WorkExperience

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_summary']

    first_name = forms.CharField(
        label="First name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'block border w-full rounded-md p-2 border-gray-400 outline-none'}),
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'block border w-full rounded-md p-2 border-gray-400 outline-none'}),
    )

    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={'class': 'block border bg-gray-200 w-full rounded-md p-2 border-gray-400 outline-none'}),
    )
    
    profile_summary = forms.CharField(
        label="Profile summary",
        widget=forms.Textarea(attrs={'class': 'block w-full h-55 rounded-md border border-gray-400 outline-none text-sm p-5 resize-none'}),
    )


class WorkHistoryForm(forms.ModelForm): 
    class Meta:
        model = WorkExperience  # Specify the associated model
        fields = ['work_title', 'company_name', 'started_month', 'started_year', 'end_month', 'end_year']
    # fields for adding work experience
    work_title = forms.CharField(
        label="Job Title",
        max_length=150,
        widget=forms.TextInput(
            attrs={'class':'w-full rounded-md border border-[#B3B3B] outline-none text-sm p-2','placeholder':'Enter your Job Title'}),
        )
    
    position = forms.CharField(
        label="Position",
        max_length=90,
        widget=forms.TextInput(
            attrs={'class':'w-full rounded-md border border-[#B3B3B] outline-none text-sm p-2','placeholder':'Enter your Job Title'})
    )
    company_name = forms.CharField(
        label="Company Name",
        max_length=150,
        widget=forms.TextInput(
            attrs={'class':'w-full rounded-md border border-[#B3B3B] outline-none text-sm p-2',
                   'placeholder':'Enter your Company Name'}),)
    started_month = forms.CharField(
        max_length=9,
        widget=forms.TextInput(
            attrs={'class':'w-max rounded-md border border-[#B3B3B] outline-none text-sm p-2',
                   'placeholder':'Enter your Start Month'}),)
    started_year = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={'class':'w-max rounded-md border border-[#B3B3B] outline-none text-sm p-2',
                   'placeholder':'Enter your Start Year'}),)
    end_month = forms.CharField(
        max_length=9,
        widget=forms.TextInput(
            attrs={'class':'w-max rounded-md border border-[#B3B3B] outline-none text-sm p-2',
                   'placeholder':'Enter your End Month'}),)
    end_year = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={'class':'w-max rounded-md border border-[#B3B3B] outline-none text-sm p-2',
                   'placeholder':'Enter your End year'}),)