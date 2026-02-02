const navItems = document.querySelectorAll(".nav-item");
const sections = document.querySelectorAll(".section");

const activateSection = (sectionId) => {
  sections.forEach((section) => {
    section.classList.toggle("active", section.id === sectionId);
  });

  navItems.forEach((item) => {
    item.classList.toggle("active", item.dataset.section === sectionId);
  });
};

navItems.forEach((item) => {
  item.addEventListener("click", () => {
    activateSection(item.dataset.section);
  });
});
