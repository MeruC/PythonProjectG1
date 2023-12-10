function onDeleteJobHandler(event, jobId) {
    event.preventDefault(); // Prevent the default form submission

    Swal.fire({
        title: "Delete Job?",
        text: "Please type CONFIRM to delete the job.",
        input: "text",
        inputAttributes: {
            autocapitalize: "off",
        },
        showCancelButton: true,
        confirmButtonText: "Delete",
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
}
