const JOB_POSTING_URL = `job_posts/?period=`;
const JOB_APPLICATION_URL = `job_applications/?period=`;

$(document).ready(function () {
  console.log("loaded dashboard.js");
  var ctx = document.getElementById("jobPostingChart").getContext("2d");
  var ctx2 = document.getElementById("jobApplicationsChart").getContext("2d");
  let chart;
  let chart2;

  initChart($("#jobPostsSelect").val());
  initApplicationChart($("#jobApplicationsSelect").val());

  $("#jobPostsSelect").on("change", function () {
    const period = $(this).val();

    initChart(period);
  });

  $("#jobApplicationsSelect").on("change", function () {
    const period = $(this).val();
    console.log(period);
    initApplicationChart(period);
  });

  async function initChart(period = "day") {
    try {
      const data = await fetchDataFromAPI(JOB_POSTING_URL + period);
      console.log(data);

      if (chart) {
        chart.destroy();
      }

      let config;

      if (period === "day") {
        // get the current date
        const date = new Date(2023, data.month - 1, 1);
        const month = date.toLocaleString("default", {
          month: "long",
        });
        $("#jobPostingLabel").text(`Job Postings for ${month}`);
        // Generate human-readable date labels (e.g., 'Dec 8', 'Dec 9', etc.)

        const readableDate = getDayDates(data.labels);
        config = jobPostingChartConfig(readableDate, data.data);
      } else if (period === "month") {
        $("#jobPostingLabel").text(`Job Postings for ${data.year}`);
        const readableDate = getMonths(data.labels);
        config = jobPostingChartConfig(readableDate, data.data);
      } else if (period === "year") {
        $("#jobPostingLabel").text(`Job Postings for All Years`);

        config = jobPostingChartConfig(data.labels, data.data);
      }

      chart = new Chart(ctx, config);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  async function initApplicationChart(period = "day") {
    try {
      const data = await fetchDataFromAPI(JOB_APPLICATION_URL + period);
      console.log(data, "what");

      if (chart2) {
        chart2.destroy();
      }

      let config;

      if (period === "day") {
        // get the current date
        const date = new Date(2023, data.month - 1, 1);
        const month = date.toLocaleString("default", {
          month: "long",
        });
        $("#jobApplicationsLabel").text(`Job Applications for ${month}`);
        // Generate human-readable date labels (e.g., 'Dec 8', 'Dec 9', etc.)

        const readableDate = getDayDates(data.labels);
        config = jobPostingChartConfig(readableDate, data.data);
      } else if (period === "month") {
        $("#jobApplicationsLabel").text(`Job Applications for ${data.year}`);
        const readableDate = getMonths(data.labels);
        config = jobPostingChartConfig(readableDate, data.data);
      } else if (period === "year") {
        $("#jobApplicationsLabel").text(`Job Applications for All Years`);

        config = jobPostingChartConfig(data.labels, data.data);
      }

      chart2 = new Chart(ctx2, config);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
});

function getDayDates(dateArr) {
  return dateArr.map((dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString("default", {
      day: "numeric",
    });
  });
}

function getMonths(dateArr) {
  return dateArr.map((dateStr) => {
    const date = new Date(2000, dateStr - 1, 1);
    return date.toLocaleString("default", {
      month: "long",
    });
  });
}

async function fetchDataFromAPI(url) {
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

function jobPostingChartConfig(labels, data) {
  return {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          data,
          label: "Job Postings",
          fill: false,
          borderColor: "#a7c957",
          tension: 0.1,
          pointRadius: 10,
          pointHoverRadius: 15,
        },
      ],
    },
    options: {
      responsive: true,
    },
  };
}
function jobPostingChartConfig(labels, data) {
  return {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          data,
          label: "Job Applications",
          fill: false,
          borderColor: "#a7c957",
          tension: 0.1,
          pointRadius: 10,
          pointHoverRadius: 15,
        },
      ],
    },
    options: {
      responsive: true,
    },
  };
}
