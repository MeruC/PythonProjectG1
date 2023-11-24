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


