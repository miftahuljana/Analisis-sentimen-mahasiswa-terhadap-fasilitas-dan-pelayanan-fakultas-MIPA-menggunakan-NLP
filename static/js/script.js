document.addEventListener("DOMContentLoaded", function () {

    let form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function () {
            document.getElementById("loading").style.display = "block";
        });
    }

});