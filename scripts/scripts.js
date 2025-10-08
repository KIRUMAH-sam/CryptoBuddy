const courses = [
  {
    id: 1,
    title: "Introduction to HTML",
    description: "Learn the basics of web structure using HTML.",
    lessons: ["Tags & Elements", "Links & Images", "Forms & Tables"],
  },
  {
    id: 2,
    title: "CSS for Beginners",
    description: "Style your web pages with colors, layouts, and animations.",
    lessons: ["Selectors & Colors", "Flexbox & Grid", "Transitions & Hover Effects"],
  },
  {
    id: 3,
    title: "JavaScript Essentials",
    description: "Make your website dynamic and interactive using JavaScript.",
    lessons: ["Variables & Functions", "DOM Manipulation", "Event Handling"],
  },
];

const authSection = document.getElementById("auth-section");
const courseList = document.getElementById("course-list");
const courseDetail = document.getElementById("course-detail");
const coursesContainer = document.getElementById("courses");
const logoutBtn = document.getElementById("logout-btn");

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const loginBtn = document.getElementById("login-btn");
const signupLink = document.getElementById("signup-link");

const courseTitle = document.getElementById("course-title");
const courseDescription = document.getElementById("course-description");
const lessonList = document.getElementById("lesson-list");
const completeBtn = document.getElementById("complete-btn");
const backBtn = document.getElementById("back-btn");

let completedCourses = JSON.parse(localStorage.getItem("completedCourses")) || [];
let currentUser = localStorage.getItem("currentUser") || null;

function showSection(section) {
  [authSection, courseList, courseDetail].forEach(sec => sec.classList.add("hidden"));
  section.classList.remove("hidden");
}

function renderCourses() {
  coursesContainer.innerHTML = "";
  courses.forEach(course => {
    const card = document.createElement("div");
    card.classList.add("course-card");

    card.innerHTML = `
      <h3>${course.title}</h3>
      <p>${course.description}</p>
      <button class="view-btn">View Course</button>
    `;

    const btn = card.querySelector(".view-btn");
    btn.addEventListener("click", () => showCourseDetail(course));

    if (completedCourses.includes(course.id)) {
      card.style.border = "2px solid #2ecc71";
    }

    coursesContainer.appendChild(card);
  });
}

function showCourseDetail(course) {
  showSection(courseDetail);
  courseTitle.textContent = course.title;
  courseDescription.textContent = course.description;
  lessonList.innerHTML = course.lessons.map(l => `<li>${l}</li>`).join("");

  completeBtn.textContent = completedCourses.includes(course.id)
    ? "Completed "
    : "Mark as Completed";
  completeBtn.classList.toggle("completed", completedCourses.includes(course.id));

  completeBtn.onclick = () => toggleCompletion(course.id);
}

function toggleCompletion(id) {
  if (completedCourses.includes(id)) {
    completedCourses = completedCourses.filter(c => c !== id);
  } else {
    completedCourses.push(id);
  }
  localStorage.setItem("completedCourses", JSON.stringify(completedCourses));
  renderCourses();
  showCourseDetail(courses.find(c => c.id === id));
}

backBtn.addEventListener("click", () => showSection(courseList));

function handleLogin() {
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();
  const users = JSON.parse(localStorage.getItem("users")) || {};

  if (!username || !password) {
    alert("Please enter both username and password.");
    return;
  }

  if (users[username] && users[username] === password) {
    localStorage.setItem("currentUser", username);
    currentUser = username;
    showDashboard();
  } else {
    alert("Invalid credentials. Try again or sign up.");
  }
}

function handleSignup() {
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();
  const users = JSON.parse(localStorage.getItem("users")) || {};

  if (!username || !password) {
    alert("Please enter both username and password.");
    return;
  }

  if (users[username]) {
    alert("User already exists! Please log in.");
    return;
  }

  users[username] = password;
  localStorage.setItem("users", JSON.stringify(users));
  alert("Signup successful! You can now log in.");
}

function showDashboard() {
  logoutBtn.classList.remove("hidden");
  renderCourses();
  showSection(courseList);
}

logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("currentUser");
  currentUser = null;
  logoutBtn.classList.add("hidden");
  showSection(authSection);
});

loginBtn.addEventListener("click", handleLogin);
signupLink.addEventListener("click", (e) => {
  e.preventDefault();
  handleSignup();
});

if (currentUser) {
  showDashboard();
} else {
  showSection(authSection);
}
