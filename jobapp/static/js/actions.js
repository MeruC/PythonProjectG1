// -------- Delete Job Confirmation Dialog --------
function onDeleteJobHandler(event, jobId) {
    event.preventDefault(); // Prevent the default form submission

    Swal.fire({
        title: "Delete Job?",
        text: "This action cannot be undone. Please type CONFIRM to delete the job.",
        icon: "warning",
        input: "text",
        inputAttributes: {
            autocapitalize: "off",
        },
        showCancelButton: true,
        confirmButtonText: "Delete",
        confirmButtonClass: "swal-confirm-button", // Add a custom class for styling
        showLoaderOnConfirm: true,
        preConfirm: (inputValue) => {
            if (inputValue === "CONFIRM") {
                // If the user typed CONFIRM, manually submit the form
                const form = document.getElementById(`deleteJobForm-${jobId}`);
                form.submit();
            } else {
                Swal.showValidationMessage("Typed text is not CONFIRM.");
            }
        },
    });

    // Add a style tag to customize the confirm button color
    const styleTag = document.createElement("style");
    styleTag.innerHTML = `
        .swal-confirm-button {
            background-color: #EF5350 !important;
        }
    `;
    document.head.appendChild(styleTag);
}

// -------- Approval and Rejection Confirmation Dialog --------

function confirmApprove(applicationId) {
    const title = 'Approve Application?';
    confirmStatusChange(applicationId, title, 'check');
}

function confirmReject(applicationId) {
    const title = 'Reject Application?';
    confirmStatusChange(applicationId, title, 'xmark');
}

function confirmStatusChange(applicationId, title, action) {
    event.preventDefault(); // Prevent the default form submission

    Swal.fire({
        title: title,
        text: `This action cannot be undone. Are you sure you want to proceed?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Confirm",
        confirmButtonClass: "swal-confirm-button",
        showLoaderOnConfirm: true,
        preConfirm: () => {
            // Manually submit the form
            const form = document.getElementById(`changeStatusForm-${applicationId}-${action}`);
            form.submit();
        },
    });

    const styleTag = document.createElement("style");
    styleTag.innerHTML = `
        .swal-confirm-button {
            background-color: ${getConfirmButtonColor(action)} !important;
        }
    `;
    document.head.appendChild(styleTag);
}

function getConfirmationTitle(action) {
    return action === 'check' ? 'Approve Application?' : (action === 'xmark' ? 'Reject Application?' : '');
}

function getConfirmButtonColor(action) {
    return action === 'check' ? '#4CAF50' : (action === 'xmark' ? '#EF5350' : '');
}
// Path: jobapp/static/js/actions.js