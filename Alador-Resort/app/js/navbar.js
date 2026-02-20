export function initNavbar() {
  const burger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");
  const links = document.querySelectorAll(".nav-links a");
  const sections = document.querySelectorAll("section");

  // 🍔 Responsive toggle
  burger?.addEventListener("click", () => {
    navLinks?.classList.toggle("active");
    burger?.setAttribute("aria-expanded", navLinks?.classList.contains("active"));
  });

  // ⌨️ Close on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      navLinks?.classList.remove("active");
      burger?.setAttribute("aria-expanded", "false");
    }
  });

  // 📱 Auto-collapse menu on link click (mobile)
  links.forEach(link => {
    link?.addEventListener("click", () => {
      navLinks?.classList.remove("active");
      burger?.setAttribute("aria-expanded", "false");
    });
  });

  // 🌐 URL hash highlight on load
  window.addEventListener("load", () => {
    const currentHash = window.location.hash;
    links.forEach(link => {
      link.classList.toggle("highlight", link.getAttribute("href") === currentHash);
    });
  });

  // 🧠 Debounced scroll for active highlighting
  let scrollTimeout;
  window.addEventListener("scroll", () => {
    if (scrollTimeout) clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      const top = window.scrollY;
      sections.forEach((section, i) => {
        const offset = section.offsetTop - 100;
        const height = section.offsetHeight;
        if (top >= offset && top < offset + height) {
          links.forEach(link => link?.classList.remove("highlight"));
          links[i]?.classList.add("highlight");
        }
      });
    }, 100); // debounce interval
  });
}