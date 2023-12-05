let selectedJobId = null;

async function getJobList() {
  try {
    const jobContentElement = document.getElementById("jobContent");
    const noJobElement = document.getElementById("noJob");
    const noDetailsElement = document.getElementById("noDetails");
    const dividerElement = document.getElementById("divider");

    const response = await fetch(`/job/getJobList`, {
      method: "GET",
    });
    if (response.ok) {
      const jsonResponse = await response.json();

      if (jsonResponse.success) {
        console.log(jsonResponse);
        if (jsonResponse.jobs.length == 0) {
          if (
            jobContentElement &&
            noJobElement &&
            noDetailsElement &&
            dividerElement
          ) {
            jobContentElement.style.display = "none";
            noJobElement.style.display = "flex";
            noDetailsElement.style.display = "none";
            dividerElement.style.display = "none";
          }
        } else {
          if (
            jobContentElement &&
            noJobElement &&
            noDetailsElement &&
            dividerElement
          ) {
            noJobElement.style.display = "none";
            jobContentElement.style.display = "flex";
            dividerElement.style.display = "flex";
            noDetailsElement.style.display = "flex";
          }

          document.getElementById("jobList").innerHTML = `
          ${jsonResponse.jobs
            .map(function (job) {
              let hasApplied = false;
              if (jsonResponse.appliedJobsId.length > 0) {
                if (jsonResponse.appliedJobsId.includes(job.id)) {
                  console.log(job.id);
                  hasApplied = true;
                }
              }
              return renderJobs(job, hasApplied);
            })
            .join("")}
        `;
        }
      }
    }
    if (selectedJobId !== null) {
      document
        .getElementById(`job-${selectedJobId}`)
        .classList.add("border-[#386641]");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

async function getJobDetails() {
  try {
    const jobId = window.location.pathname.match(/\/jobs\/(\d+)\/$/)?.[1];

    const response = await fetch(`/job/getJobDetails/${jobId}/`, {
      method: "GET",
    });

    if (response.ok) {
      const jsonResponse = await response.json();
      if (jsonResponse.success) {
        console.log(jsonResponse);
        console.log(jsonResponse.job);
        const job = jsonResponse.job;
        document.getElementById("jobTitle").innerHTML = job.job_title;
        document.getElementById("companyName").innerHTML =
          job.company__company_name;
        document.getElementById("jobDetails").innerHTML = job.description;
        document.getElementById("datePosted").innerHTML = formatDate(
          job.date_posted
        );
        document.getElementById(
          "estimatedSalary"
        ).innerHTML = `PHP ${job.min_salary.toLocaleString()} - ${job.max_salary.toLocaleString()}`;
        document.getElementById("jobType").innerHTML =
          jobType == "fulltime" ? "Full Time" : "Part-time";

        if (jsonResponse.hasApplied) {
          document.getElementById(`applyButton`).innerHTML =
            "Withraw Application";
        } else {
          document.getElementById(`applyButton`).innerHTML = "Apply Now";
        }

        document
          .querySelector("#applyButton")
          .addEventListener("click", async function () {
            jobApplication("jobDetails", jobId, jsonResponse.hasApplied);
          });
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function renderJobs(job, hasApplied) {
  return `
          <div class="job rounded-xl p-5 border-2 bg-white leading-5 shadow-sm" id="job-${
            job.id
          }" 
          onclick="handleJobClick('${job.id}', '${job.job_title}', '${
    job.company__company_name
  }', '${job.city}, ${job.country}', '${
    job.type
  }', ' PHP ${job.min_salary.toLocaleString()} - ${job.max_salary.toLocaleString()}', '${
    job.description
  }', '${formatDate(job.date_posted)}', ${hasApplied})"
          >
        <div class="text-lg font-semibold">${job.job_title}</div>

        <div class="text-gray-800">${job.company__company_name}</div>
        <div class="text-gray-800 text-sm">
          ${job.city}, ${job.country}
        </div>
        <div class="mt-2 mb-2">
          <span class="text-[#6A994E] font-semibold">
            PHP ${job.min_salary.toLocaleString()} - ${job.max_salary.toLocaleString()}
          </span>
          per month
        </div>
        <div class="inline text-xs bg-gray-300 py-1 px-2 rounded-md font-semibold">
          ${job.type == "fulltime" ? "Full Time" : "Part-time"}
        </div>

        <div class="text-gray-700 py-5">${job.description}</div>
        <div class="text-sm text-gray-700">
          Posted ${formatDate(job.date_posted)} 
        </div>
      </div>
          `;
}

async function searchJob(event) {
  event.preventDefault();
  const jobContentElement = document.getElementById("jobContent");
  const noJobElement = document.getElementById("noJob");
  const noDetailsElement = document.getElementById("noDetails");
  const dividerElement = document.getElementById("divider");
  const formElement = document.getElementById("searchJobForm");
  const formData = new FormData(formElement);
  const queryString = new URLSearchParams(formData).toString();
  const url = `/job/searchJob?${queryString}`;
  try {
    const response = await fetch(url, {
      method: "GET",
    });

    if (response.ok) {
      const jsonResponse = await response.json();

      if (jsonResponse.success) {
        console.log(jsonResponse);
        if (jsonResponse.jobs.length == 0) {
          if (
            jobContentElement &&
            noJobElement &&
            noDetailsElement &&
            dividerElement
          ) {
            jobContentElement.style.display = "none";
            noJobElement.style.display = "flex";
            noDetailsElement.style.display = "none";
            dividerElement.style.display = "none";
          }
        } else {
          if (
            jobContentElement &&
            noJobElement &&
            noDetailsElement &&
            dividerElement
          ) {
            noJobElement.style.display = "none";
            jobContentElement.style.display = "flex";
            dividerElement.style.display = "flex";
            noDetailsElement.style.display = "flex";
          }
          document.getElementById("jobList").innerHTML = `
            
          
            ${jsonResponse.jobs
              .map(function (job) {
                let hasApplied = false;

                hasApplied = true;

                return renderJobs(job, hasApplied);
              })
              .join("")}
        `;
        }
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

/* redirects the user to jobs if the window width is less than or equal to 768px (mobile)*/
function handleJobClick(
  id,
  title,
  companyName,
  location,
  jobType,
  salary,
  description,
  posted,
  hasApplied
) {
  if (window.innerWidth <= 768) {
    window.location.href = `/jobs/${id}`;
  } else {
    showJobDetails(
      id,
      title,
      companyName,
      location,
      jobType,
      salary,
      description,
      posted,
      hasApplied
    );
  }
}

function getWhatSuggestion(query) {
  const whatSuggestion = document.getElementById("whatSuggestion");
  document.getElementById("whatSuggestion").innerHTML = "";

  fetch(`/getWhatSuggestion?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      if (document.getElementById("what").value !== "") {
        if (data.success && data.suggestions.length > 0) {
          data.suggestions.forEach((suggestion) => {
            const suggestionItem = createSuggestionElement(suggestion, "what");
            whatSuggestion.appendChild(suggestionItem);
          });

          whatSuggestion.classList.remove("hidden");
        } else {
          const suggestionItem = createSuggestionElement("No result", "what");
          whatSuggestion.appendChild(suggestionItem);

          whatSuggestion.classList.remove("hidden");
        }
      } else {
        whatSuggestion.classList.add("hidden");
      }
    })
    .catch((error) => console.error("Error", error));
}

function getWhereSuggestion(query) {
  const whereSuggestion = document.getElementById("whereSuggestion");
  whereSuggestion.innerHTML = "";

  fetch(`/getWhereSuggestion?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      if (document.getElementById("where").value !== "") {
        if (data.success && data.suggestions.length > 0) {
          data.suggestions.forEach((suggestion) => {
            const suggestionItem = createSuggestionElement(suggestion, "where");
            whereSuggestion.appendChild(suggestionItem);
          });

          whereSuggestion.classList.remove("hidden");
        } else {
          const suggestionItem = createSuggestionElement("No result", "where");
          whereSuggestion.appendChild(suggestionItem);

          whereSuggestion.classList.remove("hidden");
        }
      } else {
        whereSuggestion.classList.add("hidden");
      }
    })
    .catch((error) => console.error("Error", error));
}

function createSuggestionElement(text, type) {
  const suggestionItem = document.createElement("div");
  suggestionItem.classList.add("p-2", "cursor-pointer", "hover:bg-gray-100");
  suggestionItem.textContent = text;
  if (text !== "No result") {
    suggestionItem.addEventListener("click", () => {
      document.getElementById(type == "what" ? "what" : "where").value = text;
      document
        .getElementById(type == "what" ? "whatSuggestion" : "whereSuggestion")
        .classList.toggle("hidden");
    });
  }
  return suggestionItem;
}

async function jobApplication(target, jobId, hasApplied) {
  try {
    const response = await fetch(`/job/manageApplication/${jobId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    if (response.ok) {
      const jsonResponse = await response.json();
      if (jsonResponse.success) {
        if (target == "jobDetails") {
          // getJobDetails();
          document.getElementById(`applyButton`).innerHTML = `${
            document.getElementById(`applyButton`).innerHTML == "Apply Now"
              ? "Withraw Application"
              : "Apply Now"
          }`;
        } else {
          document.getElementById(`applyButton-${jobId}`).innerHTML = `${
            document.getElementById(`applyButton-${jobId}`).innerHTML.trim() ==
            "Apply Now"
              ? "Withraw Application"
              : "Apply Now"
          }`;
          getJobList();
        }
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

/* base.html */
function showJobDetails(
  id,
  title,
  companyName,
  location,
  jobType,
  salary,
  description,
  posted,
  hasApplied
) {
  console.log(hasApplied);
  selectedJobId = id;
  document.querySelectorAll(".job").forEach((job) => {
    job.classList.remove("border-[#386641]");
  });
  console.log(hasInfo);
  document.getElementById(`job-${id}`).classList.add("border-[#386641]");
  document.getElementById("jobDetails").innerHTML = `
            <div class="min-h-full bg-white rounded-xl border border-gray-300 p-5 leading-5">
              <a href="jobs/${id}">

                <div class="text-2xl font-semibold">${title}</div>
              </a>
                <div class="text-gray-800">${companyName}</div>
                <div class="text-gray-800 text-sm">${location}</div>
                <div class="mt-2 mb-2">
                    <div class="inline text-xs bg-gray-200 py-1 px-2 rounded-md font-semibold"> 
                      ${jobType == "fulltime" ? "Full Time" : "Part-time"}</div>
                </div>
                <div>
                    <span class="text-[#6A994E] font-semibold">${salary}</span> per month
                </div>
                <div class="mt-3 mb-4">
                <button id="applyButton-${id}" class=" inline text-sm py-2 px-4  rounded-md font-semibold bg-[#BC4749] text-white disabled:cursor-not-allowed"
  onclick="jobApplication('jobList','${id}', ${hasApplied})" ${
    hasInfo == "True" ? "" : (disabled = "disabled")
  }>
  ${hasApplied == true ? "Withraw Application" : "Apply Now"}
  
</button>

<div class=" text-xs text-red-500 mt-1 ${
    hasInfo == "True" ? "hidden " : "block"
  }">
  <i class="fa-solid fa-circle-exclamation mr-1"></i>Set up 
 <a href="/profile/" class="underline">your profile</a> to apply for  job
  
  </div>
  </div>
                <div class="text-sm text-gray-700">Posted ${posted}</div>
                <hr class="my-5 bg-gray-300" />
                <h1 class="font-semibold">Job Details</h1>
                <div class="mt-2">${description}</div>
        `;
}
