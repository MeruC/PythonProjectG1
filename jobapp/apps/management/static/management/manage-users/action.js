$(document).ready(function () {
  password_toggler("new_password", "new_password_toggle", "new_password_icon");

  $("#account-activation-btn").on("click", function () {
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

  $("#change-password-form").validate({
    rules: {
      new_password: {
        required: true,
        minlength: 8, // Minimum new_password length
        hasUppercase: true,
        hasLowercase: true,
        hasNumber: true,
        hasSymbol: true,
      },
    },
    messages: {
      new_password: {
        required: "Please enter a password.",
        minlength: "Password must be at least 8 characters long.",
      },
    },

    highlight: function (element, errorClass) {
      $(element).addClass("border-red-200"); // Add a class to change the border color
    },
    unhighlight: function (element, errorClass) {
      $(element).removeClass("border-red-200"); // Remove the class to reset the border color
    },
    errorClass: "daisy-label-text-alt text-red-500",
    errorPlacement: function (error, element) {
      if (element.attr("name") == "new_password") {
        error.insertAfter("#password-container");
      }
    },
    submitHandler: function (form) {
      // Form is valid, you can submit it
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
          console.log("submitting form");
          form.submit();
        }
      });
    },
  });

  // Define custom methods for password validation
  jQuery.validator.addMethod(
    "hasUppercase",
    function (value, element) {
      // Check if the value contains at least one uppercase letter
      return /[A-Z]/.test(value);
    },
    "Password must contain at least one uppercase letter."
  );

  jQuery.validator.addMethod(
    "hasLowercase",
    function (value, element) {
      // Check if the value contains at least one lowercase letter
      return /[a-z]/.test(value);
    },
    "Password must contain at least one lowercase letter."
  );

  jQuery.validator.addMethod(
    "hasNumber",
    function (value, element) {
      // Check if the value contains at least one number
      return /\d/.test(value);
    },
    "Password must contain at least one number."
  );

  jQuery.validator.addMethod(
    "hasSymbol",
    function (value, element) {
      // Check if the value contains at least one symbol
      return /[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]/.test(value);
    },
    "Password must contain at least one symbol."
  );
});
