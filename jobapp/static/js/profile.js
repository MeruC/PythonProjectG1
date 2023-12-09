function openTab(id) {
    let profileTabBtn = $('#profile-tab-btn');
    let settingTabBtn = $('#setting-tab-btn');
    let profileTab = $('.profile-tab'); // Use a class to select the element
    let settingTab = $('.setting-tab'); // Use a class to select the element
    let activeTab = "active-tab";

    if (id === 'profile-tab-btn') {
        // Open profile tab
        settingTab.addClass('hidden');
        profileTab.removeClass('hidden');
        profileTabBtn.addClass(activeTab);
        settingTabBtn.removeClass(activeTab);
    } else if (id === 'setting-tab-btn') {
        // Open setting tab
        profileTab.addClass('hidden');
        settingTab.removeClass('hidden');
        settingTabBtn.addClass(activeTab);
        profileTabBtn.removeClass(activeTab);
    }
}

function toggleModal(action) {
    if (action === 'open-workexp-modal') $('.work-history-modal').removeClass('hidden')
    else if (action === 'open-education-modal') $('.education-modal').removeClass('hidden')
    else if (action === 'open-skill-modal') $('.skill-modal').removeClass('hidden')
    else {
        $('.work-history-modal').addClass('hidden')
        $('.education-modal').addClass('hidden')
        $('.skill-modal').addClass('hidden')
    }
}

function toggleEndWork(){
    $('.end-work-data').toggle()
}


// deleting work
function deleteWork(id,element) {
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value; //make the request POST secured
    const URL = `/profile/delWork/${parseInt(id)}/`; //link for views for deletion


    // confirmation dialog
    Swal.fire({
        title: 'Delete!',
        text: 'Are you sure you want to delete this work?',
        icon: 'error',
        confirmButtonText: 'Delete',
        confirmButtonColor: '#EF5350',
        showCancelButton: true,
        showCloseButton: true
      }).then(result=>{
        if(result.isConfirmed){
            // proceed on the deletion
            deletionProcess(URL,csrfToken,element)
        }
      })

}


function deleteEducation(id,element){
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value; //make the request POST secured
    const URL = `/profile/delEducation/${parseInt(id)}/`; //link for views for deletion


    // confirmation deletion
    // confirmation dialog
    Swal.fire({
        title: 'Delete!',
        text: 'Are you sure you want to delete this education?',
        icon: 'error',
        confirmButtonText: 'Delete',
        confirmButtonColor: '#EF5350',
        showCancelButton: true,
        showCloseButton: true
      }).then(result=>{
        if(result.isConfirmed){
            // perform the deletion of education
            element = element.parentElement
            deletionProcess(URL,csrfToken,element)
        }
      })
    

}


function deletionProcess(URL,csrfToken,element){
    fetch(URL, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response=>{return response.json()})
    .then(data => {
        // Handle the response data here if needed
        if(data.status === 200 && data.message === 'Success Deletion'){
            // delete the selected work wrapper
            const container = element.parentElement
            container.remove()
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


$(document).ready(function(){
    $('#profileInput').on('change', function () {
        let selectedFile = this.files[0];
    
        if (selectedFile) {
            let reader = new FileReader();
    
            reader.onload = function (e) { 
                $('#img_settings').attr('src', e.target.result);
            };
    
            reader.readAsDataURL(selectedFile);
        }
    });
    

    // check for password status
    $('input[name="password"]').on('input',function(){
        let currentVal = $(this).val()
        let isStrong = isStrongPassword(currentVal)

        if(isStrong){
            //indicator for strong password
            $('.weak-msg-pass').addClass('hidden')
            $('.strong-msg-pass').removeClass('hidden')
        }
        else{
             //indicator for weak password
             $('.strong-msg-pass').addClass('hidden')
             $('.weak-msg-pass').removeClass('hidden')
        }
    })


    // check the skill first
    $('#submit-skill').on('click',function(){
        const new_skill = $('input[name="skills"]').val().trim()
        const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value; //make the request POST secured
        const URL = `/profile/checkskill/${new_skill}/`; //link for views for deletion

        fetch(URL,{
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(data=>{return data.json()})
        .then(data=>{
            // assess the returned checking for newly_added skill
            if(data.status === 200 && !data.isAvailable) $('#skill-form').submit() //add the new skill
            else $('.msg-skill-error').removeClass('hidden')
        })
    })
})


function isStrongPassword(password){
    const strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return strongRegex.test(password);
}
function toggleDropdown(element){
    $('.second-dropdown').toggle()

    // change icon
    if (element.hasClass('fa-arrow-down')) {
        element.removeClass('fa-arrow-down').addClass('fa-arrow-up');
    } else {
        element.removeClass('fa-arrow-up').addClass('fa-arrow-down');
    }
}

function isLogout(){
    // confirmation
    Swal.fire({
        title: 'Sign out',
        text: 'Are you sure you want to leave?',
        icon: 'question',
        confirmButtonText: 'Sign out',
        showCancelButton: true,
        showCloseButton: true
      }).then(result=>{
        if(result.isConfirmed){
            // logout the current user
            window.open('http://127.0.0.1:8000/account/logout/','_blank')
        }
      })
}

function togglePassword(icon){

    // change icon
    if(icon.hasClass('fa-edit')) icon.removeClass('fa-edit').addClass('fa-close')
    else icon.removeClass('fa-close').addClass('fa-edit')
    
    $('.password-wrapper').toggle() //password container
}

function updatePassword(id){
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value; //make the request POST secured
    const URL = `/profile/updatePassword/${parseInt(id)}/`; //link for views for updating password
    const currentPassword = document.querySelector('input[name="current_password"]').value;
    const newPassword = $('input[name="password"]').val()
    const confirm_pass = $('input[name="confirm_pass"]').val()

    // data to be sent
    const data = {
        current_password: currentPassword,
        new_password: newPassword,
    };

    $('.unmatch-current-password-msg').addClass('hidden')
    $('.unmatch-new-password-msg').addClass('hidden')
    if(newPassword === confirm_pass && isStrongPassword(newPassword)){
        
        fetch(URL, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(response => {
            if(response.status === 200){
                // check for validation
                if(response.message === 'Password unmatched') $('.unmatch-current-password-msg').removeClass('hidden')
                else{
                    // match and updated password
                    $('.update-pass-modal').addClass('hidden')
                }
            }
        })
    
    } else
        $('.unmatch-new-password-msg').removeClass('hidden')
    
}

function togglePassModal(){
    $('.update-pass-modal').toggle()
}

function updateEducationModal(id){
    educationID = parseInt(id)
    URL = `/profile/education/${educationID}/`
    // retrieve data
    fetch(URL)
    .then(response=>{return response.json()})
    .then(response=>{
        if(response.status===200){

            // data from the database
            data = response.data[0]
            educationID = data.id
            education_level = data.education_level
            school_name = data.school_name
            course = data.course
            started_year = data.started_year
            ended_year = data.ended_year

            // set up form details for update
            $('.education-modal').removeClass('hidden')
            $('select[name="education_level"').val(education_level)
            $('input[name="school_name"').val(school_name)
            $('input[name="course"').val(course)
            $('select[name="started_year"').val(started_year)
            $('select[name="ended_year"').val(ended_year)

            $('#add-btn').addClass('hidden')
            $('#update-btn').removeClass('hidden')
                .on('click', function(){updateEducation(id)})
        }
    })
}

function updateEducation(id){
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value; //make the request POST secured
    const URL = `/profile/updateEducation/${parseInt(id)}/`; //link for views for updating password


    education_level = $('select[name="education_level"]').val();
    school_name = $('input[name="school_name"]').val();
    course = $('input[name="course"]').val();  // Corrected selector
    started_year = $('select[name="started_year"]').val();  // Corrected selector
    ended_year = $('select[name="ended_year"]').val();  // Corrected selector

    data = {
        "educationlvl": education_level,
        'school_name':school_name,
        'course':course,
        'started_year':started_year,
        'ended_year':ended_year
    }

    fetch(URL,{
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    })
    .then(response=>{return response.json()})
    .then(data=>{
        if(data.message == "Successfully updated"){
            location.reload()
        }
    })
}


function toggleDeactivateModal(){
    Swal.fire({
        title: 'Deactivate Account?',
        text: 'This action prevents you from logging in. Only the administrator will be able to activate this account. Are you sure you want to continue?',
        icon: 'error',
        confirmButtonText: 'Delete',
        confirmButtonColor: '#EF5350',
        showCancelButton: true,
        showCloseButton: true
      }).then(result=>{
        if(result.isConfirmed)$('#deact-form').submit()
      })
}