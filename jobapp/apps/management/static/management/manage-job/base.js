console.log("loaded managejobs.js!");

$(document).ready(function() {
    const dataTable = $('#jobsTable').DataTable({
        dom: 'Bfrtip',
    });

    $('#jobsSearchField').keyup(function(){
        dataTable.search($(this).val()).draw();
    });
});

function onDeleteJobHandler(jobId) {
    Swal.fire({
        title: "Delete?",
        text: "Are you sure you want to delete this record?",
        icon: "warning",
        confirmButtonText: "Delete",
        confirmButtonColor: "#EF5350",
        showCancelButton: true,
        showCloseButton: false,
      }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/management/jobs/delete/${jobId}/`;
        }
      });
}
function onEditJobHandler(jobId) {
    window.location.href = `/management/jobs/edit/${jobId}/`;
}
