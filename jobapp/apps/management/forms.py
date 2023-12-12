from datetime import datetime
from django import forms
from apps.accountapp.models import User, Education
from django.forms.widgets import ClearableFileInput
from apps.jobsapp.models import WorkExperience
from django_countries import countries


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
        widget=forms.FileInput(
            attrs={
                "class": "hidden",
                "id": "profileInput",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    # profile_img = forms.ImageField(
    #     widget=CustomClearableFileInput(
    #         attrs={
    #             "id": "profileInput",
    #             "class": (
    #                 "daisy-file-input daisy-file-input-primary "
    #                 " daisy-file-input-bordered  w-full max-w-xs block"
    #             ),
    #         }
    #     )
    # )
    first_name = forms.CharField(
        label="First name",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " lettersOnly focus:border-primary outline-none"
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
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " lettersOnly focus:border-primary outline-none"
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
                    "pl-12 form-control w-full rounded focus:ring-1"
                    " focus:ring-primary focus:border-primary outline-none"
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
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " focus:border-primary outline-none"
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
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " focus:border-primary outline-none"
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
            "job_summary",
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
                    "w-full  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded-md border border-[#B3B3B]"
                    " outline-none text-sm p-2"
                ),
                "placeholder": "Enter your Job Title",
            }
        ),
    )

    job_summary = forms.CharField(
        label="Job Summary",
        widget=forms.Textarea(
            attrs={
                "class": (
                    "  focus:ring-1 focus:ring-primary focus:border-primary"
                    " w-full rounded-md border border-[#B3B3B] outline-none"
                    " text-sm p-2"
                ),
                "placeholder": "Enter your Job Summary",
            }
        ),
    )

    company_name = forms.CharField(
        label="Company Name",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full   focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded-md border border-[#B3B3B]"
                    " outline-none text-sm p-2"
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
                    "w-max  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded-md border border-[#B3B3B]"
                    " outline-none text-sm p-2"
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
                    "w-full  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded-md border border-[#B3B3B]"
                    " outline-none text-sm p-2"
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
                    "w-max   focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded-md border border-[#B3B3B]"
                    " outline-none text-sm p-2"
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
                    "w-full  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded-md border border-[#B3B3B]"
                    " outline-none text-sm p-2"
                )
            }
        ),
    )


class EditCompanyImageForm(forms.Form):
    logo = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "",
                "id": "logo",
                "required": "false",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class EditJobForm(forms.Form):
    job_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": (
                    "form-control  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded focus:ring-1"
                    " focus:ring-primary focus:border-primary"
                ),
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": (
                    "form-control  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded focus:ring-1"
                    " focus:ring-primary focus:border-primary"
                ),
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
                "class": (
                    "form-control  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded focus:ring-1"
                    " focus:ring-primary focus:border-primary"
                ),
            },
        ),
    )

    skills = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": (
                    "form-control  focus:ring-1 focus:ring-primary"
                    " focus:border-primary rounded focus:ring-1"
                    " focus:ring-primary focus:border-primary"
                ),
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
                "class": (
                    "form-control rounded  focus:ring-1 focus:ring-primary"
                    " focus:border-primary"
                ),
                "placeholder": "",
                "autocomplete": "off",
                "required": "true",
            },
        ),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": (
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " focus:border-primary"
                ),
                "rows": 5,
                "autocomplete": "off",
                "required": "true",
            },
        ),
    )

    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "hidden",
                "id": "logo",
            }
        ),
    )

    country = forms.ChoiceField(
        choices=[("", "Select your Country")]
        + [(country, country) for code, country in countries],
        widget=forms.Select(
            attrs={
                "class": (
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " focus:border-primary"
                ),
                "autocomplete": "off",
                "required": "true",
                "id": "company_country",
            },
        ),
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": (
                    "form-control rounded focus:ring-1 focus:ring-primary"
                    " focus:border-primary"
                ),
                "autocomplete": "off",
                "required": "true",
            },
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
