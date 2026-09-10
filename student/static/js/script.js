const sidebar = document.getElementById("sidebar");
const btn = document.getElementById("toggleBtn");
const icon = document.getElementById("toggleIcon");

btn.onclick = function () {

    sidebar.classList.toggle("close");

    if (sidebar.classList.contains("close")) {
        icon.classList.remove("fa-chevron-left");
        icon.classList.add("fa-chevron-right");
    } else {
        icon.classList.remove("fa-chevron-right");
        icon.classList.add("fa-chevron-left");
    }

};