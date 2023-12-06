from django import forms
from apps.accountapp.models import User
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = "widgets/custom_profile_clearable_file_input.html"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "profile_img",
            "first_name",
            "last_name",
            "contact_number",
            "email",
            "profile_summary",
            "id",
        ]

    profile_img = forms.ImageField(
        widget=CustomClearableFileInput(
            attrs={
                "id": "profileInput",
                "class": "daisy-file-input w-full max-w-xs block",
            }
        )
    )
    first_name = forms.CharField(
        label="First name",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "block border w-full rounded-md p-2 border-gray-300"
                    " outline-none"
                )
            }
        ),
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "block border w-full rounded-md p-2 border-gray-300"
                    " outline-none"
                )
            }
        ),
    )

    contact_number = forms.CharField(
        label="Contact number",
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "block border w-full rounded-md p-2 border-gray-300"
                    " outline-none"
                )
            }
        ),
    )

    email = forms.EmailField(
        label="Email address",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": (
                    "border bg-gray-200 w-full rounded-md p-2 border-gray-300"
                    " outline-none"
                )
            }
        ),
    )

    profile_summary = forms.CharField(
        label="Profile summary",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": (
                    "block w-full h-55 rounded-md border border-gray-300"
                    " outline-none text-sm p-5 resize-none"
                )
            }
        ),
    )
