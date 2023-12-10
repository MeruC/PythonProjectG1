var momentScript = document.createElement('script');  
momentScript.setAttribute('src','https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js');
document.head.appendChild(momentScript);

function onLogoutHandler() {
  Swal.fire({
    title: "Logout?",
    text: "Are you sure you want to logout?",
    icon: "warning",
    confirmButtonText: "Logout",
    confirmButtonColor: "#EF5350",
    showCancelButton: true,
    showCloseButton: false,
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = "account/logout/";
    }
  });
}
document
  .querySelector("#dropdownIcon")
  .addEventListener("click", function (event) {
    event.preventDefault();
    document.querySelector("#dropdownContent").classList.toggle("hidden");
  });
document
  .querySelector("#notifIcon")
  .addEventListener("click", function (event) {
    event.preventDefault();
    document.querySelector("#notifContent").classList.toggle("hidden");
  });

window.addEventListener("click", function (event) {
  if (
    !document.querySelector("#notifContent").contains(event.target) &&
    !document.querySelector("#notifIcon").contains(event.target)
  ) {
    document.querySelector("#notifContent").classList.add("hidden");
  }
  if (
    !document.querySelector("#dropdownIcon").contains(event.target) &&
    !document.querySelector("#dropdownContent").contains(event.target)
  ) {
    document.querySelector("#dropdownContent").classList.add("hidden");
  }
});


// Fetching notifications

const offset = 0;

const fetchNotifications = async () => {
  console.log("Fetching notifications");

  let notificationContent;

  await fetch(`/account/notification/${offset}/`)
  .then(res=>res.json())
  .then(data=>{
    console.log(data)
    if (data.length==0){
      notificationContent = `<p class="text-center">No notifications</p>`
      return;
    }
    notificationContent = data.map(notification => {
      return `
        <li class="p-3 bg-gray-50 rounded-md">
          <a href="#">
            <div class="flex flex-row items-start gap-3">
              ${createBadge(notification.notification)}
              <div class="flex flex-col gap-1">
                <p class="font-semibold">${createNotificationTitle(notification.notification)}</p>
                <p class="text-sm text-gray-500">${notification.message}</p>
                <div class="text-xs text-gray-500">${formatDateString(notification.timestamp)}</div>
              </div>
            </div>
          </a>
        </li> 
      `
    }).join('');
  }).catch(err=>{
      console.log(err)
      notificationContent = `<p class="text-center">No notifications</p>`
  })

  document.querySelector("#notificationList").innerHTML = notificationContent;


}

document.querySelector("#notifIcon").addEventListener("click", fetchNotifications);

function createBadge(type){
  let badge = '';
  if(type === "MatchSkill"){
   return `<div class="w-8 h-8 flex items-center justify-center bg-blue-200 rounded">
            <i class="fa-solid fa-magnifying-glass text-blue-500"></i>
          </div>` 
  } else if (type === "Applicant"){
    return `<div class="w-8 h-8 flex items-center justify-center bg-green-200 rounded">
                <i class="fa-solid fa-file-invoice text-green-500"></i>
            </div>`
  } else if (type === "Application") {
    return `<div class="w-8 h-8 flex items-center justify-center bg-purple-200 rounded">
                <i class="fa-solid fa-briefcase text-purple-500"></i>
            </div>`
  } else {
    // TODO: PUT OTHER TYPE
    return badge
  }
}

function createNotificationTitle(type){
  if(type === "MatchSkill"){
    return "Skill Match"
  } else if (type === "Applicant"){
    return "New Applicant"
  } else if (type === "Application") {
    return "New Application"
  } else {
    // TODO: PUT OTHER TYPE
    return "Notification"
  }
}


function formatDateString(inputDate) {
  const currentDate = moment();
  const inputMoment = moment(inputDate).subtract(8, 'hours');
  const diffInHours = currentDate.diff(inputMoment, 'hours');
  const diffInDays = currentDate.diff(inputMoment, 'days');

  if (diffInHours <= 5) {
    return `${diffInHours} hour(s) ago`;
  } else if (diffInHours > 5 && diffInHours <= 24) {
    return inputMoment.format('hh:mmA');
  } else if (diffInDays === 1) {
    return '1 day ago';
  } else if (diffInDays > 1 && diffInDays <= 5) {
    return `${diffInDays} day(s) ago`;
  } else {
    return inputMoment.format('MMM DD, YYYY - hh:mmA');
  }
}