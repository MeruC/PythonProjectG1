$(document).ready(function () {
  $("#history-table").DataTable({
    lengthMenu: [], // Remove the entries per page dropdown
    language: {
      lengthMenu: " ", // Hide the "Show [X] entries" text
    },
    buttons: ["excel", "pdf"],
    dom: "Bfrtip",
  });

  $("#history-table").on("click", ".historyDeleteBtn", function () {
    // get the data id
    const id = $(this).data("id");
    const companyName = $(this).data("company");
    const jobTitle = $(this).data("job");

    console.log(id, companyName, jobTitle);
    Swal.fire({
      title: "Delete?",
      text: `Are you sure you want to delete their application for ${companyName} as a ${jobTitle}?`,
      icon: "warning",
      confirmButtonText: "Delete",
      confirmButtonColor: "#EF5350",
      showCancelButton: true,
      showCloseButton: false,
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = `history/${id.trim()}/delete`;
      }
    });
  });
});
