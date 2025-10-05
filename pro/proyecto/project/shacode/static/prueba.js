document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("toggleBtn");
  const sidebar = document.getElementById("sidebar");
  const resizer = document.getElementById("resizer");

  let isVisible = true;

  toggleBtn.addEventListener("click", () => {
    isVisible = !isVisible;
    sidebar.classList.toggle("hidden", !isVisible);
    toggleBtn.textContent = isVisible ? "<" : ">";
  });

  // Hacer que se pueda redimensionar
  resizer.addEventListener("mousedown", function (e) {
    document.addEventListener("mousemove", resize);
    document.addEventListener("mouseup", stopResize);
  });

  function resize(e) {
    const newWidth = e.clientX;
    if (newWidth > 100 && newWidth < 500) {
      sidebar.style.width = newWidth + "px";
    }
  }

  function stopResize() {
    document.removeEventListener("mousemove", resize);
    document.removeEventListener("mouseup", stopResize);
  }
});



// barra que permite movimiento horizontal (NO tan util)

const resizer = document.getElementById("resizer");
const sidebar = document.getElementById("sidebar");
const container = document.querySelector(".chat-container");

let isResizing = false;

resizer.addEventListener("mousedown", function (e) {
  isResizing = true;
  document.body.style.cursor = "col-resize";
});

document.addEventListener("mousemove", function (e) {
  if (!isResizing) return;

  const newWidth = e.clientX - sidebar.getBoundingClientRect().left;
  if (newWidth > 150 && newWidth < 500) { // límites opcionales
    sidebar.style.width = `${newWidth}px`;
  }
});

document.addEventListener("mouseup", function () {
  isResizing = false;
  document.body.style.cursor = "default";
});


// ver password
 function toggleVisibility(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (input.type === "password") {
      input.type = "text";
      icon.textContent = "> ᴗ <";
    } else {
      input.type = "password";
      icon.textContent = "⊙ ‿ ⊙";
    }
  }
