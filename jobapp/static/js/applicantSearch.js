document.addEventListener('DOMContentLoaded', function () {
    // Attach an input event listener to the search box
    document.getElementById('search').addEventListener('input', function () {
      // Get the search term from the input box
      var search_term = this.value.toLowerCase();

      // Get all rows in the table body
      var rows = document.getElementById('applicant-table-body').getElementsByTagName('tr');

      // Loop through each row and hide/show based on the search term
      for (var i = 0; i < rows.length; i++) {
        var fullName = rows[i].getElementsByTagName('td')[0].textContent.toLowerCase();
        var email = rows[i].getElementsByTagName('td')[1].textContent.toLowerCase();
        var dateApplied = rows[i].getElementsByTagName('td')[2].textContent.toLowerCase();
        var status = rows[i].getElementsByTagName('td')[3].textContent.toLowerCase();

        // Check if any of the columns contain the search term
        if (
          fullName.includes(search_term) ||
          email.includes(search_term) ||
          dateApplied.includes(search_term) ||
          status.includes(search_term)
        ) {
          rows[i].style.display = '';
        } else {
          rows[i].style.display = 'none';
        }
      }
    });
  });