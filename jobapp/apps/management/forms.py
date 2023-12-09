from datetime import datetime
from django import forms
from apps.accountapp.models import User, Education
from django.forms.widgets import ClearableFileInput
from apps.jobsapp.models import WorkExperience


class CustomClearableFileInput(ClearableFileInput):
    template_name = "widgets/custom_profile_input.html"


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
                "class": (
                    "daisy-file-input daisy-file-input-primary "
                    " daisy-file-input-bordered  w-full max-w-xs block"
                ),
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


# form field for education
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            "education_level",
            "school_name",
            "course",
            "started_year",
            "ended_year",
            "id",
        ]

    @staticmethod
    def get_year():
        years = []

        # Get year from the current year to 1980
        today = datetime.today()
        current_year = today.year
        stopping_year = 1980
        step = -1

        for i in range(current_year, stopping_year + step, step):
            years.append((i, str(i)))

        return years

    options = Education.DEGREE_LEVEL_CHOICES
    education_level = forms.ChoiceField(
        label="Education Level",
        choices=options,
        widget=forms.Select(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                )
            }
        ),
        required=True,
    )

    school_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your school",
            }
        ),
        required=True,
    )

    course = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your course",
            }
        ),
        required=True,
    )

    started_year = forms.ChoiceField(
        choices=get_year(),
        widget=forms.Select(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                )
            }
        ),
        required=True,
    )

    ended_year = forms.ChoiceField(
        choices=get_year(),
        widget=forms.Select(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                )
            }
        ),
        required=True,
    )

    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


# form field for work
class WorkHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkExperience  # Specify the associated model
        fields = [
            "work_title",
            "company_name",
            "started_month",
            "started_year",
            "end_month",
            "end_year",
        ]

    @staticmethod
    def get_year():
        years = []

        # Get year from the current year to 1980
        today = datetime.today()
        current_year = today.year
        stopping_year = 1980
        step = -1

        for i in range(current_year, stopping_year + step, step):
            years.append((i, str(i)))

        return years

    STARTED_MONTH_CHOICES = [
        ("Jan", "January"),
        ("Feb", "February"),
        ("Mar", "March"),
        ("Apr", "April"),
        ("May", "May"),
        ("Jun", "June"),
        ("Jul", "July"),
        ("Aug", "August"),
        ("Sep", "September"),
        ("Oct", "October"),
        ("Nov", "November"),
        ("Dec", "December"),
    ]

    # fields for adding work experience
    work_title = forms.CharField(
        label="Job Title",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your Job Title",
            }
        ),
    )

    position = forms.CharField(
        label="Position",
        max_length=90,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your Job Title",
            }
        ),
    )
    company_name = forms.CharField(
        label="Company Name",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your Company Name",
            }
        ),
    )
    started_month = forms.ChoiceField(
        choices=STARTED_MONTH_CHOICES,
        widget=forms.Select(
            attrs={
                "class": (
                    "w-max rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your Start Month",
            }
        ),
    )

    started_year = forms.ChoiceField(
        choices=get_year(),
        widget=forms.Select(
            attrs={
                "id": "started-year",
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
            }
        ),
    )

    end_month = forms.ChoiceField(
        choices=STARTED_MONTH_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": (
                    "w-max rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your End Month",
            }
        ),
    )

    end_year = forms.ChoiceField(
        choices=get_year(),
        widget=forms.Select(
            attrs={
                "class": (
                    "w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                )
            }
        ),
    )
