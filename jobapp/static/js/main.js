/* used in async calls, gets the csrf token */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

/* formats the date to a human readable format */
function formatDate(dateString) {
  console.log("formatDate called",dateString);
  if (!dateString) return "Unknown";

  var now = new Date();
  var date = new Date(dateString);

  var timeDifferenceMinutes = Math.floor((now - date) / (1000 * 60));

  if (timeDifferenceMinutes < 60) {
    // Less than an hour ago
    return humanizeDuration(now - date) + " ago";
  } else if (timeDifferenceMinutes < 12 * 60) {
    // Less than 12 hours ago
    return formatTime(date);
  } else if (timeDifferenceMinutes < 24 * 60) {
    // Less than 24 hours ago
    return "Yesterday at " + formatTime(date);
  } else {
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }
}

function humanizeDuration(duration) {
  var minutes = Math.floor(duration / (1000 * 60));
  return minutes + " minute" + (minutes === 1 ? "" : "s");
}

function formatTime(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? " PM" : " AM";

  hours = hours % 12;
  hours = hours ? hours : 12;

  return hours + ":" + (minutes < 10 ? "0" : "") + minutes + ampm;
}
