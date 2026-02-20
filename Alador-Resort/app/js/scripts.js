document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (!hamburger || !navLinks) {
    console.warn("Hamburger menu elements not found.");
    return;
  }
});

  // =====================
  // Leaflet Map Initialization
  // =====================
  const map = L.map('map').setView([CONFIG,9.03, 38.74], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  L.marker([9.03, 38.74]).addTo(map)
  .bindPopup('Addis Ababa')
  .openPopup();

  const localeTexts = {
  en: {
    greeting: ["Happy New Year!", "Spring Serenity 🌸", "Summer Bliss 🌞", "Autumn Escape 🍂", "Winter Wonderland ❄️"]
    popup: "Addis Ababa"
  },
  am: {
    greeting: ["መልካም አዲስ ዓመት!", "የጸዳል ክፍል 🌸", ...],
    popup: "አዲስ አበባ"
  }
};


  // =====================
  // Hamburger Menu Toggle
  // =====================
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");
  hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });

  // =====================
  // Carousel Navigation
  // =====================
  let currentIndex = 0;
  const slideContainers = document.querySelectorAll('.slide-container');
  const dots = document.querySelectorAll('.dot');

  function showSlide(index) {
    if (index >= slideContainers.length) currentIndex = 0;
    else if (index < 0) currentIndex = slideContainers.length - 1;
    else currentIndex = index;

    slideContainers.forEach((slide, i) => {
      slide.style.display = i === currentIndex ? 'block' : 'none';
    });

    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentIndex);
    });
  }

  function changeSlide(n) {
    showSlide(currentIndex + n);
  }

  function currentSlide(n) {
    showSlide(n);
  }

  showSlide(currentIndex);

  // =====================
  // Lightbox Interaction
  // =====================
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const galleryImages = document.querySelectorAll('.gallery img');

  galleryImages.forEach(img => {
    img.addEventListener('click', () => {
      lightboxImg.src = img.src;
      lightbox.classList.add('show');
    });
  });

  window.closeLightbox = function () {
    lightbox.classList.remove('show');
    lightboxImg.src = "";
  };

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === "Escape") closeLightbox();
  });

  // =====================
  // Scroll-triggered Fade-ins
  // =====================
  const fadeElements = document.querySelectorAll('.fade-in');
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  fadeElements.forEach(el => fadeObserver.observe(el));

  // =====================
  // Stat Counter Animation
  // =====================
  const counters = document.querySelectorAll('.counter');
  let countersStarted = false;

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !countersStarted) {
        counters.forEach(counter => animateCounter(counter));
        countersStarted = true;
      }
    });
  }, { threshold: 0.3 });
  const CONFIG = {
  mapCoords: [9.03, 38.74],
  scrollOffset: 100,
  fadeThreshold: 0.2,
  counterStepDivisor: 100,
};

  counters.forEach(counter => counterObserver.observe(counter));

  function animateCounter(counter) {
    const target = +counter.getAttribute('data-target');
    let count = 0;
    const step = Math.ceil(target / 100);
    const interval = setInterval(() => {
      count += step;
      if (count >= target) {
        counter.textContent = target;
        clearInterval(interval);
      } else {
        counter.textContent = count;
      }
    }, 20);
  }

  // =====================
  // Scroll-aware Nav Highlight
  // =====================
  const sections = document.querySelectorAll("section[id]");
  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY + 100;
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      const id = section.getAttribute("id");
      const navLink = document.querySelector(`.nav-links a[href="#${id}"]`);
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        navLink?.classList.add("active");
      } else {
        navLink?.classList.remove("active");
      }
    });
  });

  // =====================
  // Parallax Background Scroll
  // =====================
  const parallaxBg = document.querySelector(".parallax-bg");
  window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    if (parallaxBg) {
      parallaxBg.style.transform = `translateY(${scrollTop * 0.3}px)`;
    }

    const navbar = document.querySelector(".navbar");
    if (scrollTop > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });
});