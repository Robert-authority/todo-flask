// animasi halus saat page load
document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll("[data-task]");

  items.forEach((item, i) => {
    item.style.opacity = "0";
    item.style.transform = "translateY(10px)";

    setTimeout(() => {
      item.style.transition = "all 0.25s ease";
      item.style.opacity = "1";
      item.style.transform = "translateY(0)";
    }, i * 60);
  });
});
