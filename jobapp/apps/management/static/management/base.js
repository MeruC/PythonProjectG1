/**
 * Use this file to edit js configuration that is affected on the whole base_management html.
 */
$(document).ready(function () {
  // handles the logout functionality
 // $("#logoutBtn").on("click", logout);
});

function logout() {
  // make a sweet alert dialog
  Swal.fire({
    title: "Logout",
    text: "You will be logged out",
    icon: "info",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes please",
  }).then((result) => {
    if (result.isConfirmed) {
      setTimeout(() => {
        window.location.href = "/account/logout";
      }, 500); // Adjust the delay time as needed
    }
  });
}
