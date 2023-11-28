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
    else {
        $('.work-history-modal').addClass('hidden')
        $('.education-modal').addClass('hidden')
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
        text: 'This is a SweetAlert dialog.',
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
        text: 'This is a SweetAlert dialog.',
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
    
})

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

