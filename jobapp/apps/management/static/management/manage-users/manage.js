console.log("loaded manageusers.js!");

window.document.addEventListener("DOMContentLoaded", function () {
  handleEventListeners();
});

async function handleEventListeners() {
  $(".educationEditModalBtn").click(async function (e) {
    e.preventDefault();
    const id = $(this).data("education-id");
    console.log(id);
    const data = await updateEducationData(id);
    populateEducationModal(data);
    document.querySelector("#educationModal").showModal();
  });

  $("#updateEducationbtn").click(function (e) {
    handleEducationConfirmation();
  });
  $(".educationDeleteModalBtn").click(function (e) {
    e.preventDefault();
    handleEducationDeleteConfirmation();
  });
}

async function handleEducationConfirmation() {
  const educationModal = document.querySelector("#educationModal");
  educationModal.close();

  const res = await Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, edit it!",
  });

  if (res.isConfirmed) {
    // run some post form submission code here
    $("#education_form").submit();
  } else {
    educationModal.showModal();
  }
}

async function handleEducationDeleteConfirmation() {
  const res = await Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, delete it!",
  });

  if (res.isConfirmed) {
    // get the form
    $("#deleteEducationForm").submit();
  } else {
  }
}

function populateEducationModal(data) {
  data = data.data[0];
  educationID = data.id;
  education_level = data.education_level;
  school_name = data.school_name;
  course = data.course;
  started_year = data.started_year;
  ended_year = data.ended_year;
  console.log(data);
  $('select[name="education_level"').val(education_level);
  $('input[name="school_name"').val(school_name);
  $('input[name="course"').val(course);
  $('select[name="started_year"').val(started_year);
  $('select[name="ended_year"').val(ended_year);
  $("#education_id").attr("value", educationID);
}

// copied from profile.js
async function updateEducationData(id) {
  educationID = parseInt(id);
  const URL = `/profile/education/${educationID}/`;
  // retrieve data
  const response = await fetch(URL);
  const data = await response.json();
  if (response.status === 200) {
    return data;
  } else {
    console.log("Error retrieving data");
    return null;
  }
}
