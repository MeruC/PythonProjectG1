$(document).ready(function () {
  password_toggler("new_password", "new_password_toggle", "new_password_icon");

  $("#account-activation-btn").on("click", function () {
    // make a sweet alert dialog confirmation
    Swal.fire({
      title: "Confirm Account Activation?",
      text: "Are you sure you want to activate this account?",
      icon: "info", // question, warning, error, success
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, activate it",
    }).then((result) => {
      if (result.isConfirmed) {
        // run some post form submission code here
        $("#activate-form").submit();
      }
    });
  });

  $("#account-deactivation-btn").on("click", function () {
    // make a sweet alert dialog confirmation
    Swal.fire({
      title: "Confirm Account Deactivation?",
      text: "Are you sure you want to deactivate this account?",
      icon: "info", // question, warning, error, success
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, deactivate it",
    }).then((result) => {
      if (result.isConfirmed) {
        // run some post form submission code here
        $("#deactivate-form").submit();
      }
    });
  });

  $("#updatePassBtn").on("click", function () {
    // make a sweet alert dialog confirmation
    Swal.fire({
      title: "Confirm Password Change?",
      text: "Are you sure you want to change the password of this account?",
      icon: "info", // question, warning, error, success
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, change it",
    }).then((result) => {
      if (result.isConfirmed) {
        // run some post form submission code here
        $("#change-password-form").submit();
      }
    });
  });
});
