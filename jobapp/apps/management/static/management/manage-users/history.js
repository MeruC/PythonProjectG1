$(document).ready(function () {
  $("#history-table").DataTable({
    lengthMenu: [], // Remove the entries per page dropdown
    language: {
      lengthMenu: " ", // Hide the "Show [X] entries" text
    },
  });
});
