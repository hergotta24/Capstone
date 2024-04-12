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
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
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

// Attach the redirectToReviewPage function to the button's click event
document.getElementById('product_review').addEventListener('click', redirectToReviewPage);

$('#add_to_cart').click(function (e) {
    e.preventDefault(); // Prevent default form submission

    // Gather data from elements
    var formData = {'quantity': document.getElementById('quantity').value}

    // Send form data using fetch post request
    fetch('/products/' + document.getElementById('add_to_cart').value + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Function to get CSRF token
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
            setTimeout(function () {
                window.location.href = "/";
            }, 4000); // 3000 milliseconds = 3 seconds
        })
        .catch(error => {
            console.error('Error:', error);
            let errorMessage = typeof error.message === 'object' ? Object.values(error.message).join(" ") : error.message;
        });

    function getCookie(name)
    {
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
});
