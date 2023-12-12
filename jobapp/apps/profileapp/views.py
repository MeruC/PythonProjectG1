from datetime import timezone
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import (
    EditForm,
    WorkHistoryForm,
    EducationForm,
    PasswordForm,
    SkillForm,
)
from django.shortcuts import get_object_or_404, render, redirect
from apps.jobsapp.models import WorkExperience
from apps.accountapp.models import ActivityLog, Education, User
from django.core.exceptions import ValidationError
from ..accountapp.views import Login, hasUnreadNotif
from django.contrib.auth import logout
from fpdf import FPDF


# retrieve current user data
def get_user_data(request):
    return {
        "email": request.user.email,
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "profile_summary": request.user.profile_summary,
        "profile_img": request.user.profile_img,
        "skills": formatted_skill(request.user.skills)
        if request.user.skills
        else [],
    }


# retrieve all the work experience of user
def get_user_work_experience(request):
    user = request.user.id
    work_experience = WorkExperience.objects.filter(user=user)
    return work_experience


# retrieve all the education
def get_user_education(request):
    user = request.user.id
    education = Education.objects.filter(user=user)
    return education


@login_required(login_url="/account/login/")
def index(request):
    if request.method == "POST":
        form = EditForm(
            request.POST, request.FILES, instance=request.user
        )  # instance of the current user
        work_history_form = WorkHistoryForm(
            request.POST
        )  # Pass request.POST here, not just request
        education_form = EducationForm(request.POST)
        password_form = PasswordForm(request.POST)
        skill_form = SkillForm(request.POST)
        if form.is_valid():  # checking if there's an error
            try:
                form.save()  # update the data of the current user
                ActivityLog.objects.create(
                    user=request.user,
                    action="Update Profile",
                    timestamp=timezone.now(),
                )
                messages.success(request, "Profile successfully updated.")
                return redirect(
                    "profileapp:index"
                )  # direct only to the profile again
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(
                request, "Profile update failed. Please check the form."
            )

    else:
        form = EditForm(instance=request.user)
        work_history_form = (
            WorkHistoryForm()
        )  # Create a blank instance for rendering in the template
        education_form = EducationForm()
        password_form = PasswordForm()
        skill_form = SkillForm()

    # data of the current user to be displayed on the profile section
    template = "profile.html"
    user_data = get_user_data(request)
    work_experiences = get_user_work_experience(request)
    education = get_user_education(request)

    hasInfo = (
        request.user.email
        and request.user.id
        and request.user.username
        and request.user.first_name
        and request.user.last_name
        and request.user.profile_summary
        and request.user.profile_img
        and request.user.skills
        and education
    )
    missingList = []
    if not request.user.profile_summary:
        missingList.append("Profile Summary")
    if not request.user.profile_img:
        missingList.append("Profile Image")
    if not request.user.skills:
        missingList.append("Skills")
    if not education:
        missingList.append("Education")

    missingList = ", ".join(missingList)

    context = {
        "user_data": user_data,
        "form": form,
        "work_form": work_history_form,
        "work_experiences": work_experiences,
        "education": education_form,
        "education_data": education,
        "password_form": password_form,
        "skill_form": skill_form,
        "hasUnreadNotif": hasUnreadNotif(request),
        "hasInfo": hasInfo,
        "missingList": missingList,
    }

    return render(request, template, context)


# user skill
def formatted_skill(skills):
    # separate each skill
    skills_arr = skills.split(",")
    return skills_arr


def retrieveEducation(request, id):
    education = Education.objects.filter(id=id).values()
    education_list = list(education)
    return JsonResponse({"status": 200, "data": education_list}, safe=False)


def addWorkExp(request):
    if request.method == "POST":
        work_history_form = WorkHistoryForm(
            request.POST
        )  # Pass request.POST here, not just request

        if work_history_form.is_valid():
            try:
                # work history form data field
                start_month = request.POST.get("started_month")
                start_year = request.POST.get("started_year")
                start_date = f"{start_month}, {start_year}"

                is_present = request.POST.get("present")

                end_month = request.POST.get("end_month")
                end_year = request.POST.get("end_year")
                end_date = f"{end_month}, {end_year}"
                job_summary = request.POST.get("job_summary")
                company_name = request.POST.get("company_name")

                # add new data to the database
                work_experience = work_history_form.save(commit=False)
                # check if the present is clicked
                work_experience.end_date = "Present" if is_present else end_date
                work_experience.start_date = start_date
                work_experience.job_summary = job_summary
                work_experience.user = request.user
                work_experience.company_name = company_name
                work_experience.save()  # add the new work experience
                ActivityLog.objects.create(
                    user=request.user,
                    action="Update Profile",
                    timestamp=timezone.now(),
                )
                messages.success(request, "Work experience successfully added.")
                return redirect("profileapp:index")
            except ValidationError as e:
                messages.error(
                    request, "Profile update failed. An error occurred."
                )
                print(e)

    else:
        work_history_form = (
            WorkHistoryForm()
        )  # Create a blank instance for rendering in the template

    # data of the current user to be displayed on the profile section
    user_data = get_user_data(request)
    template = "profile.html"
    context = {"user_data": user_data, "work_form": work_history_form}
    return render(request, template, context)


def addEducation(request):
    if request.method == "POST":
        form = EditForm(
            request.POST, instance=request.user
        )  # instance of the current user
        work_history_form = WorkHistoryForm(
            request.POST
        )  # Pass request.POST here, not just request
        education_form = EducationForm(request.POST)

        if education_form.is_valid():
            try:
                # add new record of education
                new_education = education_form.save(commit=False)
                new_education.user = request.user
                new_education.save()
                ActivityLog.objects.create(
                    user=request.user,
                    action="Update Profile",
                    timestamp=timezone.now(),
                )
                messages.success(request, "Education successfully added.")
                return redirect(
                    "profileapp:index"
                )  # Redirect to the profile again
            except Exception as e:
                messages.error(request, "Education update failed")

    user_data = get_user_data(request)
    template = "profile.html"
    work_experiences = get_user_work_experience(request)
    context = {
        "user_data": user_data,
        "form": form,
        "work_form": work_history_form,
        "work_experiences": work_experiences,
        "education": education_form,
    }

    return render(request, template, context)


def addSkill(request):
    if request.method == "POST":
        try:
            current_skill = request.user.skills  # skill of the user
            added_skill = request.POST.get("skills")

            # concatenating the skills already available (if any) in the newly added skill
            new_skill = (
                f"{current_skill},{added_skill}"
                if current_skill != ""
                else added_skill
            )
            User.objects.filter(username=request.user.username).update(
                skills=new_skill
            )  # update skill data
            ActivityLog.objects.create(
                user=request.user,
                action="Update Profile",
                timestamp=timezone.now(),
            )
            messages.success(request, "Skill successfully added.")
        except Exception as e:
            messages.error(request, "Error: {e}")
    return redirect("profileapp:index")


def check_current_password(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)

        try:
            # load body to get the data sent
            data = json.loads(request.body)
            current_password = data.get("current_password")
            user_auth = authenticate(
                request, username=user.username, password=current_password
            )

            # check current password for validation
            if user_auth is not None:
                return JsonResponse(
                    {"status": 200, "message": "Password matched"}
                )
            else:
                return JsonResponse(
                    {"status": 200, "message": "Password unmatched"}
                )

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("profileapp:index")  # Redirect to the profile again

    return redirect("profileapp:index")


def update_password(request):
    if request.method == "POST":
        new_password = request.POST.get("password")

        # update password
        try:
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password successfully updated.")
        except Exception as e:
            messages.error(request, f"Erro: {e}")

    return redirect("profileapp:index")


def updateEducation(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            educationlvl = data.get("educationlvl")
            school_name = data.get("school_name")
            course = data.get("course")
            started_year = data.get("started_year")
            ended_year = data.get("ended_year")

            # update the data
            Education.objects.filter(id=id).update(
                education_level=educationlvl,
                school_name=school_name,
                course=course,
                started_year=started_year,
                ended_year=ended_year,
            )
            ActivityLog.objects.create(
                user=request.user,
                action="Update Profile",
                timestamp=timezone.now(),
            )
            messages.success(request, "Education successfully updated.")
            return JsonResponse(
                {"status": 200, "message": "Successfully updated"}
            )
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("profileapp:index")


# deleting record


# ------ work deletion
def delete_work(request, id):
    del_work = get_object_or_404(WorkExperience, id=id)
    try:
        del_work.delete()  # delete the selected data in the record
        messages.success(request, "Work successfully removed.")
        return JsonResponse({"status": 200, "message": "Success Deletion"})
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect("profileapp:index")


# -----------education deletion
def delete_education(request, id):
    del_education = get_object_or_404(Education, id=id)
    try:
        del_education.delete()  # delete education record
        messages.success(request, "Education successfully removed.")
        return JsonResponse({"status": 200, "message": "Success Deletion"})
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect("profileapp:index")


# ===== Skill Deletion
def delete_skill(request, skill):
    try:
        current_ID = request.user.id
        user_skill = User.objects.get(id=current_ID)
        skills_arr = formatted_skill(
            user_skill.skills
        )  # format the string into array

        skills_arr.remove(skill)  # remove specific item in the list
        updated_skill = ",".join(skills_arr)

        User.objects.filter(id=current_ID).update(
            skills=updated_skill
        )  # update the skill data
        messages.success(request, "Skill successfully removed.")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect("profileapp:index")


# ===========Check if the newly added skill is already existing
def isSkillAvailable(request, skill):
    if request.method == "POST":
        try:
            user_obj = User.objects.get(id=request.user.id)
            current_skill = formatted_skill(user_obj.skills)  # format into list
            isAvailable = True if skill in current_skill else False

            return JsonResponse({"status": 200, "isAvailable": isAvailable})
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("profileapp:index")

    return redirect("profileapp:index")


# deactivate account
def DeactivateAccount(request):
    if request.method == "POST":
        try:
            current_id = request.user.id
            User.objects.filter(id=current_id).update(is_deactivated=True)
            messages.success(request, "Account successfully deactivated")

            # direct logout
            logout(request)
            return redirect("accountapp:login")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return redirect("profileapp:index")


def gresume(request):
    return HttpResponse("Hello world!")


CELL_WIDTH = 0


# generate pdf
def resume(request):
    # VARIABLES
    userN = (
        "_".join(request.user.last_name.split(" "))
        + "_"
        + "_".join(request.user.first_name.split(" "))
        + "_Resume"
    )

    profile_img = request.user.profile_img
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    contact_no = request.user.contact_number
    profile_sum = request.user.profile_summary

    # GETS EVERY WORK EXPERIENCE
    work_experiences = get_user_work_experience(request)
    if work_experiences:
        last_work = work_experiences[len(work_experiences) - 1]

    # GETS EVERY EDUCATION
    education = get_user_education(request)
    last_education = education[len(education) - 1]

    skills = ", ".join(i for i in request.user.skills.split(","))

    # CREATES PDF
    pdf = FPDF("P", "mm", "A4")

    pdf.set_title(last_name + ", " + first_name + " Resume")
    pdf.set_author("WorkIt Job Portal")

    # HANDLES PAGE BREAKS
    pdf.set_auto_page_break(auto=True, margin=15)
    # ADD PAGE
    pdf.add_page()

    ###HEADER
    # PROFILE PICTURE
    pdf.set_fill_color(56, 102, 65)
    pdf.rect(0, 0, 210, 40, style="F")
    pdf.image(profile_img, 170, 8, 25)

    # NAME
    pdf.set_font("helvetica", "", 24)
    pdf.set_text_color(230, 230, 230)
    pdf.cell(0, 4, "", border=False, ln=1, align="L")
    pdf.cell(0, 7, first_name + " " + last_name, border=False, ln=1, align="L")

    # EMAIL
    pdf.set_text_color(180, 180, 180)
    pdf.set_font("helvetica", "", 14)
    pdf.cell(0, 7, email, ln=1, align="L")

    # PHONE NUMBER
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 4, "+63" + contact_no, ln=1, align="L")
    pdf.ln(20)

    ###PROFILE SUMMARY
    # TITLE
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(97, 178, 113)
    pdf.cell(0, 5, "Profile Summary", ln=True)

    # Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)

    ##SUMMARY CONTENT
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5, "\t\t\t\t\t\t\t\t\t" + profile_sum, align="J")

    ###WORK EXPERIENCE
    # TITLE
    pdf.cell(1, 48, "")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(97, 178, 113)
    pdf.cell(0, 5, "Work Experience", ln=True)

    # Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)

    if work_experiences:
        for work in work_experiences:
            # WORK TITLE
            pdf.cell(1, 48, "")
            pdf.set_font("helvetica", "", 18)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 8, work.work_title, ln=True)

            # COMPANY NAME
            pdf.cell(10, 8, "")
            pdf.set_font("helvetica", "", 14)
            pdf.set_text_color(97, 178, 113)
            company_width = pdf.get_string_width(work.company_name)
            pdf.cell(company_width + 1, 8, work.company_name)

            # DIVIDER
            pdf.set_font("helvetica", "", 12)
            pdf.set_text_color(75, 75, 75)
            pdf.cell(4, 8, "\t|\t")

            # START AND END DATES
            pdf.set_font("helvetica", "", 8)
            date = work.start_date + " to " + work.end_date
            pdf.cell(40, 9, date, ln=True)

            # JOB SUMMARY
            pdf.set_font("helvetica", "", 12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(
                0,
                5,
                "\t\t\t\t\t\t\t\t\t" + work.job_summary,
                align="J",
                ln=True,
            )
            pdf.set_text_color(50, 50, 50)

            # MINI LINE BREAK
            if work != last_work:
                pdf.cell(
                    0,
                    8,
                    "--------------------------------------------------------------------------------------------------------------------------------------",
                    ln=True,
                    align="C",
                )
    else:
        pdf.cell(1, 48, "")
        pdf.set_font("helvetica", "", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "NO WORK EXPERIENCE", ln=True)

    ###EDUCATION
    # TITLE
    pdf.cell(1, 48, "")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(97, 178, 113)
    pdf.cell(0, 5, "Education", ln=True)

    # Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)

    for edu in education:
        # SCHOOL NAME
        pdf.cell(1, 48, "")
        pdf.set_font("helvetica", "", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(100, 8, edu.school_name, ln=True)

        # EDUCATION LEVEL
        pdf.cell(10, 8, "")
        pdf.set_font("helvetica", "", 14)
        pdf.set_text_color(97, 178, 113)
        level_width = pdf.get_string_width(edu.get_education_level_display())
        pdf.cell(level_width + 1, 8, edu.get_education_level_display())

        # DIVIDER
        pdf.set_font("helvetica", "", 12)
        pdf.set_text_color(75, 75, 75)
        pdf.cell(4, 8, "\t|\t")

        # START AND END DATES
        pdf.set_font("helvetica", "", 8)
        date = str(edu.started_year) + " to " + str(edu.ended_year)
        pdf.cell(40, 9, date, ln=True)

        # COURSE
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(10, 4, "")
        pdf.cell(40, 4, edu.course, ln=True)
        pdf.set_text_color(50, 50, 50)

        # MINI LINE BREAK
        if edu != last_education:
            pdf.cell(
                0,
                8,
                "--------------------------------------------------------------------------------------------------------------------------------------",
                ln=True,
                align="C",
            )

    ###SKILLS
    pdf.cell(1, 30, "")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(97, 178, 113)
    pdf.cell(0, 5, "Skills", ln=True)

    # Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)

    pdf.set_font("helvetica", "", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5, "\t\t\t\t\t\t\t\t\t\t" + skills, align="J")

    # OUTPUT
    response = HttpResponse(
        bytes(pdf.output()),
        content_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=" + userN + ".pdf"},
    )
    return response
