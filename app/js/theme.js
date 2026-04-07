export function applySeasonalTheme() {
  const month = new Date().getMonth();
  const header = document.getElementById("seasonal-header");
  const greetingElement = document.getElementById("seasonal-greeting");

  const seasonalThemes = [
    {
      name: "winter",
      months: [11, 0, 1],
      greeting: "❄️ Cozy Winter Wishes from Alador Resort",
      headline: "Welcome to Alador Resort — your cozy winter haven.",
      background: "/static/images/header_winter.jpg"
    },
    {
      name: "spring",
      months: [2, 3, 4],
      greeting: "🌸 Spring Serenity Awaits You",
      headline: "Welcome to Alador Resort — your spring sanctuary of elegance.",
      background: "/static/images/header_spring.jpg"
    },
    {
      name: "summer",
      months: [5, 6, 7, 8],
      greeting: "☀️ Bright Summer Days Await You",
      headline: "Welcome to Alador Resort — your sun-kissed summer escape.",
      background: "/static/images/header_summer.jpg"
    },
    {
      name: "autumn",
      months: [9, 10],
      greeting: "🍂 Discover Comfort in Every Season",
      headline: "Welcome to Alador Resort — your warm autumn retreat.",
      background: "/static/images/header_autumn.jpg"
    }
  ];

  const currentTheme = seasonalThemes.find(season => season.months.includes(month)) || seasonalThemes[3]; // default to autumn

  document.body.classList.add(`${currentTheme.name}-theme`);
  if (header) header.style.backgroundImage = `url('${currentTheme.background}')`;
  if (greetingElement) greetingElement.textContent = currentTheme.greeting;

  const seasonalGreetingFallback = document.getElementById('seasonal-greeting');
  if (seasonalGreetingFallback) seasonalGreetingFallback.textContent = currentTheme.headline;
}