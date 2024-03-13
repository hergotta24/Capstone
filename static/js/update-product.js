
$(document).ready(function() {
    $('#update-product').on('click', function(event) {
        event.preventDefault();

        // Retrieve form data
        const productName = $('#product-name').val();
        const productPrice = $('#product-price').val();
        const productQOH = $('#product-qoh').val();
        const productDescription = $('#product-description').text();

        const formData = {
            product_name: productName,
            price: productPrice,
            qoh: productQOH,
            description: productDescription
        }
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
                // If the update was successful, you may want to redirect the user or show a success message
                console.log("Product updated successfully");
            } else {
                // If there's an error, handle it accordingly
                console.error("Failed to update product");
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

function makeToast(message, status) {
    var toast = document.getElementById("toast");
    var bgColor = "";
    if (status == 200) {
        bgColor = "bg-success";
    } else if (status == 400) {
        bgColor = "bg-danger";
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