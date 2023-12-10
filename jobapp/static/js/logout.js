
function onLogoutHandler() {
  Swal.fire({
    title: "Logout?",
    text: "Are you sure you want to logout?",
    icon: "warning",
    confirmButtonText: "Logout",
    confirmButtonColor: "#EF5350",
    showCancelButton: true,
    showCloseButton: false,
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = "/account/logout/";
    }
  });
}
