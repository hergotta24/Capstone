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

function checkQuantityChange(input) {
    var initialQuantity = input.defaultValue;
    var updateBtn = input.parentNode.querySelector('.update-btn');

    if (input.value != initialQuantity) {
        updateBtn.style.display = 'inline-block';
    } else {
        updateBtn.style.display = 'none';
    }
}

$(document).ready(function() {
    // Use a class selector for the update buttons
    $('.update-btn').on('click', function(event) {
        event.preventDefault();

        // Retrieve the product ID associated with the clicked button
        const productId = $(this).data('product-id');

        // Find the corresponding quantity input for the clicked button
        const newQty = $(this).siblings('.quantity-input').val();

        const formData = {
            productId: productId,
            newQty: newQty
        }

        console.log(formData);

        // Send form data using fetch post request
        fetch('/updateCartQty/', {
            method: "POST",
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
            },
        })
        .then(response => {
            if (response.ok) {
                console.log("Quantity updated");
                return response.json();
            } else {
                return response.json().then(data => Promise.reject(data));
            }
        })
        .then(data => {
            console.log(data);
            makeToast(data.message, 200);
            setTimeout(function () {
                window.location.href = `/cart/`;
            }, 1500); // 3000 milliseconds = 3 seconds
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // Use a class selector for the quantity inputs and attach onchange event handler
    $('.quantity-input').on('change', function() {
        var initialQuantity = this.defaultValue;
        var updateBtn = $(this).siblings('.update-btn')[0]; // Select the corresponding update button

        if (this.value !== initialQuantity) {
            updateBtn.style.display = 'inline-block';
        } else {
            updateBtn.style.display = 'none';
        }
    });
});

function makeToast(message, status) {
    console.log(message);
    console.log(status);
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