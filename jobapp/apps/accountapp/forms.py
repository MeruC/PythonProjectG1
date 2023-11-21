# forms.py
from django import forms
from .utils import check_identifier, is_valid_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    identifier = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "juandelacruz or juandelacruz@email.com",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "••••••••",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")

        if identifier and password:
            identifier_field = check_identifier(identifier)

            try:
                user = User.objects.get(**{identifier_field: identifier})

                if not check_password(password, user.password):
                    self.add_error(
                        "password", forms.ValidationError("Password is incorrect.")
                    )

            except User.DoesNotExist:
                # self.add_error(None, forms.ValidationError("Account does not exist."))
                self.add_error(
                    "identifier", forms.ValidationError("Account does not exist.")
                )

        return cleaned_data


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "Juan",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "Dela Cruz",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "juandelacruz",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "juandelacruz@email.com",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "••••••••",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "rounded-md w-full mt-1 py-2 px-3 border border-gray-300 focus:outline-none focus:border-[#6A994E]",
                "placeholder": "••••••••",
                "autocomplete": "off",
                "required": "true",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and not is_valid_password(password):
            self.add_error("password", "")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Password did not match.")

        if User.objects.filter(username=username).exists():
            self.add_error("username", "Username is already taken.")

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email is already taken.")

        return cleaned_data
