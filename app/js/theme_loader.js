// 🌍 Seasonal Weather Theme Loader

document.addEventListener("DOMContentLoaded", () => {
  // 🌤 Date-based themes
  const month = new Date().getMonth();
  const body = document.body;
  const header = document.getElementById("seasonal-header");
  const greeting = document.getElementById("seasonal-greeting");

  const themes = {
    winter: { months: [11, 0, 1], class: "winter-theme", image: "header_winter.jpg", text: "❄️ Cozy Winter Wishes" },
    spring: { months: [2, 3, 4], class: "spring-theme", image: "header_spring.jpg", text: "🌸 Spring Serenity" },
    summer: { months: [5, 6, 7, 8], class: "summer-theme", image: "header_summer.jpg", text: "☀️ Bright Summer Days" },
    autumn: { months: [9, 10], class: "autumn-theme", image: "header_autumn.jpg", text: "🍂 Autumn Escape" }
  };

  const current = Object.values(themes).find(t => t.months.includes(month));
  if (current) {
    body.classList.add(current.class);
    if (header) header.style.backgroundImage = `url('/static/images/${current.image}')`;
    if (greeting) greeting.textContent = current.text;
  }

  // 🌧 Optional: if server provides weather, you can map it to a class
  try {
    if (window.__weather && Array.isArray(window.__weather.weather) && window.__weather.weather.length > 0) {
      const condition = window.__weather.weather[0].main.toLowerCase();
      body.classList.add(condition);
    }
  } catch (e) { /* ignore */ }
});