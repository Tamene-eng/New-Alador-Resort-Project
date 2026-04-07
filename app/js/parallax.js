export function initParallax() {
  const layers = document.querySelectorAll(".parallax-bg");

  let ticking = false;

  function updateParallax() {
    const scrollY = window.scrollY;

    layers.forEach(layer => {
      const speed = parseFloat(layer.dataset.speed) || 0.5;
      layer.style.transform = `translateY(${scrollY * speed}px)`;
    });

    ticking = false;
  }

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(updateParallax);
      ticking = true;
    }
  });
}