document.addEventListener("DOMContentLoaded", function() {
    var peachArray = document.getElementById("peachArray");
    var grapeArray = document.getElementById("grapeArray");

    for (var i = 1; i <= 5; i++) {
        var peachImg = document.createElement("img");
        peachImg.src = '/static/images/plants/peach_healthy/image (' + i + ').JPG';
        peachArray.appendChild(peachImg);

        var grapeImg = document.createElement("img");
        grapeImg.src = '/static/images/plants/grape_healthy/image (' + i + ').JPG';
        grapeArray.appendChild(grapeImg);
    }

    document.getElementById("peachButton").addEventListener("click", function() {
        submitAnswer("peach");
    });

    document.getElementById("grapeButton").addEventListener("click", function() {
        submitAnswer("grape");
    });

    function submitAnswer(answer) {
        var data = {
            answer: answer
        };

        fetch("/submit_answer", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
            window.location.href = "/bonus";
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }
});
