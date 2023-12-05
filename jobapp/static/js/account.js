function password_toggler(password_id, passwordToggleId, eyeIconId) {
  const password_input = document.getElementById(password_id);
  const password_toggle = document.getElementById(passwordToggleId);
  const password_icon = document.getElementById(eyeIconId);

  password_toggle.addEventListener("click", () => {
    if (password_input.type === "password") {
      password_input.type = "text";
      password_icon.classList.remove("fa-eye");
      password_icon.classList.add("fa-eye-slash");
    } else {
      password_input.type = "password";
      password_icon.classList.remove("fa-eye-slash");
      password_icon.classList.add("fa-eye");
    }
  });
}

function password_requirment(password_id, requirement_id) {
  const password_input = document.getElementById(password_id);
  const requirement_div = document.getElementById(requirement_id);

  function updateRequirementDisplay(password) {
    const meets_Requirement = checkPasswordRequirement(password);
    requirement_div.classList.toggle("text-red-500", !meets_Requirement);
    requirement_div.style.display = meets_Requirement ? "none" : "block";
  }

  const initial_password = password_input.value;
  if (initial_password !== "") {
    updateRequirementDisplay(initial_password);
  }

  password_input.addEventListener("input", function () {
    updateRequirementDisplay(password_input.value);
  });

  function checkPasswordRequirement(password) {
    if (password.length < 8 || password.length > 20) {
      return false;
    }
    const has_upperCase = /[A-Z]/.test(password);
    const has_lowerCase = /[a-z]/.test(password);
    const has_number = /\d/.test(password);
    const has_symbol = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]/.test(password);

    return has_upperCase && has_lowerCase && has_number && has_symbol;
  }
}
