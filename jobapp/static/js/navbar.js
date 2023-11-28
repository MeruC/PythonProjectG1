document
  .querySelector("#icon_dropdown")
  .addEventListener("click", function (event) {
    event.preventDefault();
    document.querySelector("#dropdown").classList.toggle("hidden");
  });

window.addEventListener("click", function (event) {
  if (
    !document.querySelector("#icon_dropdown").contains(event.target) &&
    !document.querySelector("#dropdown").contains(event.target)
  ) {
    document.querySelector("#dropdown").classList.add("hidden");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const logoutLink = document.getElementById("logout-link");
  const confirmationModal = document.getElementById("confirmation-modal");
  const confirmLogoutButton = document.getElementById("confirm-logout");
  const cancelLogoutButton = document.getElementById("cancel-logout");

  logoutLink.addEventListener("click", function (event) {
    event.preventDefault();
    confirmationModal.style.display = "flex";
  });

  confirmLogoutButton.addEventListener("click", function () {
    window.location.href = logoutLink.querySelector("a").href;
  });

  cancelLogoutButton.addEventListener("click", function () {
    confirmationModal.style.display = "none";
  });
});
