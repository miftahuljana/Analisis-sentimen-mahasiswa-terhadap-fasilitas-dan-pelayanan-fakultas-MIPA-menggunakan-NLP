document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("uploadForm");

    if(form){

        form.addEventListener("submit", function(){

            document.getElementById("loading-screen")
                .style.display = "flex";

        });

    }

});