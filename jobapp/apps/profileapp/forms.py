from django import forms
from apps.accountapp.models import User

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
