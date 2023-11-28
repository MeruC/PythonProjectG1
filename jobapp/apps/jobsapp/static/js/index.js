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
  document.querySelectorAll(".job").forEach((job) => {
    job.classList.remove("border-[#386641]");
  });
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
                
                <button id="applyButton" class="inline text-sm py-2 px-4 mt-3 mb-4 rounded-md font-semibold bg-[#BC4749] text-white"
  onclick="jobApplication(,'jobList''${id}', ${hasApplied})">
  ${hasApplied == true ? "Unapply" : "Apply Now"}
  
</button>

                <div class="text-sm text-gray-700">Posted ${posted}</div>
                <hr class="my-5 bg-gray-300" />
                <h1 class="font-semibold">Job Details</h1>
                <div class="mt-2">${description}</div>
        `;
}

async function jobApplication(target, jobId, hasApplied) {
  console.log(hasApplied);
  let url = hasApplied == true ? `removeApplication` : `submitApplication`;
  console.log(url);
  try {
    const response = await fetch(`/job/${url}/${jobId}/`, {
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
          getJobDetails();
        } else {
          getJobList();
        }
        document.getElementById("applyButton").innerHTML = `${
          hasApplied == true ? "Apply Now" : "Unapply"
        }`;
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
async function getJobList() {
  try {
    const response = await fetch(`/job/getJobList`, {
      method: "GET",
    });
    if (response.ok) {
      const jsonResponse = await response.json();

      if (jsonResponse.success) {
        console.log(jsonResponse);
        if (jsonResponse.jobs.length == 0) {
          document.getElementById("jobContent").style.display = "none";
          document.getElementById("noDetails").style.display = "none";
        } else {
          document.getElementById("jobContent").style.display = "flex";
          document.getElementById("noDetails").style.display = "flex";

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
          document.getElementById("applyButton").innerHTML = "Unapply";
        } else {
          document.getElementById("applyButton").innerHTML = "Apply Now";
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

async function searchJob(event) {
  event.preventDefault();

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
          document.getElementById("jobList").classList.add("md:w-1/2");
          document.getElementById("jobList").classList.remove("md:w-1/2");
        } else {
          document.getElementById("jobList").classList.remove("md:w-1/2");
          document.getElementById("jobList").classList.add("md:w-1/2");
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
  document.getElementById("whatSuggestion").innerHTML = "";

  fetch(`/getWhatSuggestion?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.suggestions.length > 0) {
        console.log(data);
        data.suggestions.forEach((suggestion) => {
          const suggestionItem = document.createElement("div");
          suggestionItem.classList.add(
            "p-2",
            "cursor-pointer",
            "hover:bg-gray-100"
          );
          suggestionItem.textContent = suggestion;
          suggestionItem.addEventListener("click", () => {
            document.getElementById("what").value = suggestion;

            document.getElementById("whatSuggestion").classList.add("hidden");
          });
          document.getElementById("whatSuggestion").appendChild(suggestionItem);
        });

        document.getElementById("whatSuggestion").classList.remove("hidden");
      } else {
        document.getElementById("whatSuggestion").classList.add("hidden");
      }
    })
    .catch((error) => {
      console.error("Error fetching suggestions:", error);
    });
}
function getWhereSuggestion(query) {
  document.getElementById("whereSuggestion").innerHTML = "";

  fetch(`/getWhereSuggestion?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.suggestions.length > 0) {
        console.log(data);
        data.suggestions.forEach((suggestion) => {
          const suggestionItem = document.createElement("div");
          suggestionItem.classList.add(
            "p-2",
            "cursor-pointer",
            "hover:bg-gray-100"
          );
          suggestionItem.textContent = suggestion;
          suggestionItem.addEventListener("click", () => {
            document.getElementById("where").value = suggestion;

            document.getElementById("whereSuggestion").classList.add("hidden");
          });
          document
            .getElementById("whereSuggestion")
            .appendChild(suggestionItem);
        });

        document.getElementById("whereSuggestion").classList.remove("hidden");
      } else {
        document.getElementById("whereSuggestion").classList.add("hidden");
      }
    })
    .catch((error) => {
      console.error("Error", error);
    });
}
