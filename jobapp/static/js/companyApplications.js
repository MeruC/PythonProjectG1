// DataTables Initialization
$(document).ready(function() {
  const jobsTable = $('#jobsTable').DataTable({
      dom: 'Bfrtip',
      "autoWidth": false,
      "columnDefs": [
          { "width": "20%", "targets": 0 },
          { "width": "25%", "targets": 1 },
          { "width": "20%", "targets": 2 },
          { "width": "15%", "targets": 3 },
          { "width": "10%", "targets": 4 },
          { "width": "20%", "targets": 5 },
      ],
      buttons: [
          {
              extend: 'pdf',
              exportOptions: {
                  columns: [0, 1, 2, 3, 4, 5, 6]
              },
              title: 'Job Listings',
              customize: function(doc) {
                  // change table header background color
                  doc.content[1].table.headerRows = 1;
                  doc.content[1].table.widths = Array(doc.content[1].table.body[0].length).fill('auto');
                  doc.content[1].table.body[0].forEach(function(column, index) {
                      column.fillColor = '#3866411';
                  });

                  // set specific widths for the columns
                  doc.content[1].table.widths = ['*', '*', '15%', '15%', '10%'];

                  // align table header to left
                  const header = doc.content[1].table.body[0];
                  header.forEach(cell => {
                      cell.alignment = 'left';
                  });

                  // add margin to each cell
                  const tableBody = doc.content[1].table.body;
                  tableBody.forEach(row => {
                      row.forEach(cell => {
                          cell.margin = [5, 5, 5, 5];
                      });
                  });

                  // footer
                  doc.footer = function(page, pages) {
                      return {
                          text: [
                              { text: `Generated by: ${generatedBy}\n`, alignment: 'left' },
                              {
                                  text: 'Date Generated: ' + new Date().toLocaleString('en-US', {
                                      month: 'long',
                                      day: '2-digit',
                                      year: 'numeric',
                                      hour: 'numeric',
                                      minute: 'numeric',
                                      hour12: true
                                  }), alignment: 'left'
                              }
                          ],
                          margin: [40, 0],
                          fontSize: 10
                      };
                  };
              }
          },
      ]
  });

  $('#jobsSearchField').keyup(function() {
      jobsTable.search($(this).val()).draw();
  });

  // ... (your existing code)
});


