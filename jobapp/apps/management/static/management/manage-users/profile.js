$(document).ready(function () {
  // form validation
  $("#profile-form").validate(formOptions);
  // make it only accept letters
  $(".lettersOnly").keyup(function () {
    // do not accept numbers else accept it
    if (this.value.match(/[^a-zA-Z ]/g)) {
      this.value = this.value.replace(/[^a-zA-Z ]/g, "");
    }
  });
});

const formOptions = {
  rules: {
    first_name: {
      required: true,
    },
    last_name: {
      required: true,
    },
    profile_summary: {
      required: true,
    },
    email: {
      required: true,
      email: true,
    },
    contact_number: {
      required: true,
      number: true,
      minlength: 10,
      maxlength: 12,
    },
  },
  messages: {
    first_name: {
      required: "Please enter your first name",
    },
    last_name: {
      required: "Please enter your last name",
    },
    profile_summary: {
      required: "Please enter your profile summary",
    },
    email: {
      required: "Please enter your email address",
      email: "Please enter a valid email address",
    },
    contact_number: {
      required: "Please enter your phone number",
      number: "Please enter a valid phone number",
      minlength: "Phone number should be at least 10 digits",
      maxlength: "Phone number should not exceed 12 digits",
    },
  },
  highlight: function (element, errorClass) {
    $(element).addClass("border-red-500"); // Add a class to change the border color
    $(element).removeClass("border-green-500");
  },
  unhighlight: function (element, errorClass) {
    $(element).removeClass("border-red-500"); // Remove the class to reset the border color
    $(element).addClass("border-green-500");
  },
  errorClass: "daisy-label-text-alt text-red-500 block",

  submitHandler: function (form) {
    handleProfileConfirmation(form);
  },
};

function handleProfileConfirmation(form) {
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
      form.submit();
    }
  });
}

// document.getElementById('profilePicture').addEventListener('change', function () {
//   var selectedFile = this.files[0];

//   if (selectedFile) {
//       var reader = new FileReader();

//       reader.onload = function (e) {
//           document.getElementById('profileInput').src = e.target.result;
//       };

//       reader.readAsDataURL(selectedFile);
//   }
// });
