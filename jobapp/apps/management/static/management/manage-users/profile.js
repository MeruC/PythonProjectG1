$(document).ready(function () {
  $("#update-profile-btn").on("click", function () {
    // make a sweet alert dialog confirmation
    Swal.fire({
      title: "Confirm Edit Information?",
      text: "Are you sure you want to edit your information?",
      icon: "info", // question, warning, error, success
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, edit it",
    }).then((result) => {
      if (result.isConfirmed) {
        // run some post form submission code here
        $("#profile-form").submit();
      }
    });
  });
});
