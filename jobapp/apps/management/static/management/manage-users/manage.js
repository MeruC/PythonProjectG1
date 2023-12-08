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

  $(".workEditModalBtn").click(async function (e) {
    e.preventDefault();
    const id = $(this).data("work-id");
    console.log(id);
    const data = await updateWorkData(id);
    populateWorkModal(data);
    document.querySelector("#workModal").showModal();
  });

  $("#updateEducationbtn").click(function (e) {
    handleEducationConfirmation();
  });

  $("#updateWorknbtn").click(function (e) {
    handleWorkConfirmation();
  });

  $(".educationDeleteModalBtn").click(function (e) {
    e.preventDefault();
    handleEducationDeleteConfirmation();
  });

  $(".workDeleteModalBtn").click(function (e) {
    e.preventDefault();
    handleWorkDeleteConfirmation();
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

async function handleWorkConfirmation() {
  const workModal = document.querySelector("#workModal");
  workModal.close();

  const res = await Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, edit work!",
  });

  if (res.isConfirmed) {
    // run some post form submission code here
    $("#work_form").submit();
  } else {
    workModal.showModal();
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

async function handleWorkDeleteConfirmation() {
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
    $("#deleteWorkForm").submit();
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

function populateWorkModal(resData) {
  console.log(resData);
  const data = resData.data;
  const split_start_date = data.start_date.split(", ");
  const split_end_date = data.end_date.split(", ");
  const workID = data.id;
  const work_title = data.work_title;
  const company_name = data.company_name;
  const position = data.position;
  const started_month = split_start_date[0];
  const started_year = split_start_date[1];
  const end_month = split_end_date[0];
  const end_year = split_end_date[1];

  console.log(data);
  $('input[name="work_title"').val(work_title);
  $('input[name="company_name"').val(company_name);
  $('input[name="position"').val(position);
  $('select[name="started_month"').val(started_month);
  $('select[name="started_year"').val(started_year);
  $('select[name="end_month"').val(end_month);
  $('input[name="end_year"').val(end_year);
  $("#work_id").attr("value", workID);
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

// copied from profile.js
async function updateWorkData(id) {
  id = parseInt(id);
  const URL = `/management/job_history/${id}`;
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
