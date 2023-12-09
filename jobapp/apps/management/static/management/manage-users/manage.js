$(document).ready(function () {
  $("#user-table").DataTable({
    lengthMenu: [], // Remove the entries per page dropdown
    language: {
      lengthMenu: " ", // Hide the "Show [X] entries" text
    },
    buttons: ["excel", "pdf"],
    dom: "Bfrtip",
  });
});
