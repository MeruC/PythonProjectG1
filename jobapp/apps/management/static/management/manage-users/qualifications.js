console.log("loaded manageusers.js!");

window.document.addEventListener("DOMContentLoaded", function () {
  handleEventListeners();
  $("#education_form").validate({
    messages: {
      education_level: {
        required: "Please enter your education level",
      },
      school_name: {
        required: "Please enter your school name",
      },
      course: {
        required: "Please enter your course",
      },
      started_year: {
        required: "Please enter your started year",
      },
      ended_year: {
        required: "Please enter your ended year",
      },
    },
    highlight: function (element, errorClass) {
      $(element).addClass("border-red-500"); // Add a class to change the border color
    },
    unhighlight: function (element, errorClass) {
      $(element).removeClass("border-red-500"); // Remove the class to reset the border color
      // $(element).addClass("border-green-500");
    },
    errorClass: "daisy-label-text-alt text-red-500",

    submitHandler: function (form) {
      handleEducationConfirmation(form);
    },
  });

  // Custom validation method for ensuring a select has a value selected
  $.validator.addMethod(
    "requiredSelect",
    function (value, element) {
      return value !== ""; // Validate that the value is not an empty string (the default empty option)
    },
    "Please select an option"
  );
  $("#work_form").validate({
    rules: {
      work_title: {
        required: true,
      },
      company_name: {
        required: true,
      },
      job_summary: {
        required: true,
      },
    },
    messages: {
      work_title: {
        required: "Please enter your work title",
      },
      company_name: {
        required: "Please enter your company name",
      },
      job_summary: {
        required: "Please enter your job summary",
      },
    },
    highlight: function (element, errorClass) {
      $(element).addClass("border-red-500"); // Add a class to change the border color
    },
    unhighlight: function (element, errorClass) {
      $(element).removeClass("border-red-500"); // Remove the class to reset the border color
    },
    errorClass: "daisy-label-text-alt text-red-500",

    submitHandler: function (form) {
      handleWorkConfirmation(form);
    },
  });
});

function toggleEndWork() {
  $(".end-work-data").toggle();
}

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

  $(".education-container .edit-btns").on(
    "click",
    ".form-container",
    function (e) {
      //prevent propagation
      e.stopPropagation();
      e.preventDefault();
      // get the child form
      const form = $(this).children("form");
      console.log(form);
      console.log(this);
      handleEducationDeleteConfirmation(form);
    }
  );

  $(".work-container .edit-work-btns").on(
    "click",
    ".form-container",
    function (e) {
      //prevent propagation
      e.stopPropagation();
      e.preventDefault();
      // get the child form
      const form = $(this).children("form");
      console.log(form);
      console.log(this);
      handleWorkDeleteConfirmation(form);
    }
  );
}

async function handleEducationConfirmation(form) {
  const educationModal = document.querySelector("#educationModal");
  educationModal.close();
  document.querySelector("#education_confirmation_modal").showModal();

  $("#confirmEducationEditBtn").click(function (e) {
    e.preventDefault();
    form.submit();
  });

  $("#cancelEducationEditBtn").click(function (e) {
    educationModal.showModal();
  });
}

async function handleWorkConfirmation(form) {
  const workModal = document.querySelector("#workModal");
  workModal.close();
  document.querySelector("#work_confirmation_modal").showModal();

  $("#confirmWorkEditBtn").click(function (e) {
    e.preventDefault();
    form.submit();
  });

  $("#cancelWorkEditBtn").click(function (e) {
    workModal.showModal();
  });
}

async function handleEducationDeleteConfirmation(form) {
  const res = await Swal.fire({
    title: "Remove Education History?",
    text: "Are you sure to remove this education history?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, remove it!",
  });

  if (res.isConfirmed) {
    // get the form
    form.submit();
  } else {
  }
}

async function handleWorkDeleteConfirmation(form) {
  const res = await Swal.fire({
    title: "Remove Work Experience?",
    text: "Are you sure to remove this work experience?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, remove it!",
  });

  if (res.isConfirmed) {
    // get the form
    form.submit();
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
  const job_summary = data.job_summary;
  const started_month = split_start_date[0];
  const started_year = split_start_date[1];
  const end_month = split_end_date[0];
  const end_year = split_end_date[1];
  console.log(split_start_date);
  console.log(split_end_date);

  console.log(data);
  $('input[name="work_title"').val(work_title);
  $('input[name="company_name"').val(company_name);
  $('textarea[name="job_summary"').val(job_summary);
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
