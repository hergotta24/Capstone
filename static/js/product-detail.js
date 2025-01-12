let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    console.log("it's working")
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("demo");
    let captionText = document.getElementById("caption");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

// Define a function to handle the button click event
function redirectToReviewPage() {
    // Get the product ID from the button's value attribute
    var productId = document.getElementById('product_review').value;

    // Construct the URL for redirection
    var redirectUrl = '/review-product/' + productId;

    // Redirect the browser to the constructed URL
    window.location.href = redirectUrl;
}

$('#product_review').on('click', redirectToReviewPage);


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

function toggleReview() {
    let reviewForm = document.getElementById('reviewDiv');
    let leaveReviewBtn = document.getElementById('leaveReviewBtn');

    reviewForm.style.display = reviewForm.style.display === 'none' ? 'block' : 'none';
    reviewForm.disabled = !reviewForm.disabled;
    leaveReviewBtn.innerHTML = leaveReviewBtn.innerHTML === 'Write a Review' ? 'Cancel' : 'Write a Review';
}

$(document).ready(function () {
    $('#add_to_cart').on('click', function(event) {

        var formData = {'quantity': $('#quantity').val()};

        fetch('/products/' + $(this).val() + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                console.log("Card input success");
                return response.json();
            } else {
                return response.json().then(data => Promise.reject(data));
            }
        })
        .then(data => {
            console.log("Response data:", data);
            setTimeout(function () {

            }, 4000); // 4000 milliseconds = 4 seconds
        })
        .catch(error => {
            console.error('Error:', error);
            let errorMessage = typeof error.message === 'object' ? Object.values(error.message).join(" ") : error.message;
            console.error('Error Message:', errorMessage);
        });
    });
});

function toggleReview() {
            let reviewForm = document.getElementById('reviewDiv');
            let leaveReviewBtn = document.getElementById('leaveReviewBtn');

            reviewForm.style.display = reviewForm.style.display === 'none' ? 'block' : 'none';
            reviewForm.disabled = !reviewForm.disabled;
            leaveReviewBtn.innerHTML = leaveReviewBtn.innerHTML === 'Write a Review' ? 'Cancel' : 'Write a Review';
        }

        // Define a function to handle the button click event
        function redirectToReviewPage() {
            // Get the product ID from the button's value attribute
            var productId = document.getElementById('product_review').value;

            // Construct the URL for redirection
            var redirectUrl = '/review-product/' + productId;

            // Redirect the browser to the constructed URL
            window.location.href = redirectUrl;
        }
