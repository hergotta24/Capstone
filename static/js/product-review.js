let rating = 0

$(document).ready(function () {


    $('#review-product').on('click', function (event) {
        event.preventDefault();

        // Retrieve form data
        const comment = $('#comment').text();

        const formData = {
            rating: rating,
            comment: comment
        }
        // console.log(formData);

        let url = window.location.pathname

        // Send form data using fetch post request
        fetch(url, {
            method: "POST",
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
            },
        })
            .then(response => {
                if (response.ok) {
                    console.log("Review created");
                    return response.json();
                } else {
                    return response.json().then(data => Promise.reject(data));
                }
            })
            .then(data => {
                // console.log(data);
                makeToast(data.message, 200);
                setTimeout(function () {
                    window.location.href = `/products/${product_id}`;
                }, 3000); // 3000 milliseconds = 3 seconds
            })
            .catch(error => {
                console.error("Error:", error);
                let errorMessage = typeof error.message === 'object' ? Object.values(error.message).join(" ") : error.message;
                makeToast(errorMessage, 400);
            });
    });
});

const stars =
    document.getElementsByClassName("star");
let selected = ['fa-solid', 'checked']
let unselected = ['fa-regular', 'unchecked']
let hovered = ['fa-solid', 'checked']

//Function to update rating
function updateRating(n) {
    remove();

    for (let i = 0; i < n; i++) {
        if (n === 1) rating = 1
        else if (n === 2) rating = 2
        else if (n === 3) rating = 3
        else if (n === 4) rating = 4
        else if (n === 5) rating = 5

        stars[i].classList.remove(...unselected)
        stars[i].classList.add(...selected)
    }
}

// To remove the pre-applied styling
function remove() {
    for (let i = 0; i < 5; i++) {
        stars[i].className = "star fa fa-star fa-lg fa-regular unchecked"
    }
}

function mouseOver(n) {
    remove();

    for (let i = 0; i < n; i++) {
        stars[i].classList.remove(...unselected)
        stars[i].classList.add(...hovered)
    }
}

function mouseOff() {
    remove();

    for (let i = 0; i < rating; i++) {

        stars[i].classList.remove(...unselected)
        stars[i].classList.add(...selected)
    }
}

// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function makeToast(message, status) {
    // console.log(message);
    // console.log(status);
    var toast = document.getElementById("toast");
    var bgColor = "";
    if (status == 200) {
        bgColor = "bg-success";
        toast.classList.remove("bg-danger");
    } else if (status == 400) {
        bgColor = "bg-danger";
        toast.classList.remove("bg-success");
    }
    toast.classList.add(bgColor)

    var toastBody = toast.querySelector('.toast-body');

    // Set the message
    toastBody.textContent = message;

    // Show the toast
    var bootstrapToast = new bootstrap.Toast(toast);
    bootstrapToast.show();

    setTimeout(function () {
        if (status == 200) {
            bootstrapToast.hide();
            toast.classList.remove(bgColor);
            toastBody.textContent = "";
        }
    }, 4000);
}