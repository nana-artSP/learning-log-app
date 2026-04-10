async function login() {
    const username = document.getElementById("loginId").value;
    const password = document.getElementById("loginPw").value;

    const correctId = "alice";
    const correctPw = "1234";

    if (username === correctId && password === correctPw) {
        sessionStorage.setItem("loggedIn", "yes");
        location.href = "profile.html";
    } else {
        document.getElementById("error").textContent = "残念違うよ♡";
    }
}

function updateClock() {
  const now = new Date();
  const time = now.toLocaleTimeString();
  document.getElementById("clock").textContent = time;
}

setInterval(updateClock, 1000);

const toggle = document.getElementById("modeToggle");

toggle.addEventListener("click", function () {

  document.body.classList.toggle("dark");

  if (document.body.classList.contains("dark")) {
    localStorage.setItem("mode", "dark");
  } else {
    localStorage.setItem("mode", "light");
  }

});

const startDate = new Date("2026-03-06");
const today = new Date();

const diff = today - startDate;

const days = Math.floor(diff / (1000 * 60 * 60 * 24));

document.getElementById("studyDays").textContent =
"学習日数 Day " + days;


let minutes = localStorage.getItem("studyMinutes");

if (minutes === null) {
  minutes = 0;
} else {
  minutes = Number(minutes);
}

function addStudy() {

  minutes += 30;

  localStorage.setItem("studyMinutes", minutes);

  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;

  document.getElementById("studyTime").textContent =
  "Today Study " + hours + "h " + mins + "m";

}

function updateStudyDisplay() {

  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;

  document.getElementById("studyTime").textContent =
  "Today Study " + hours + "h " + mins + "m";

}

// 保存されたモードを読み込む
const savedMode = localStorage.getItem("mode");

if (savedMode === "dark") {
  document.body.classList.add("dark");
}

// 最初に実行
updateStudyDisplay();