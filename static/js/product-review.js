
$(document).ready(function() {
    $('#review-product').on('click', function(event) {
        event.preventDefault();

        // Retrieve form data
        const rating = $('#rating').val();
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
            if (response.ok || response.redirected) {
                // If the update was successful, you may want to redirect the user or show a success message
                console.log("Thanks for your review!");
            } else {
                // If there's an error, handle it accordingly
                console.error("Failed to leave review");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});

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