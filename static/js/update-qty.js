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

$(document).ready(function() {
    // Use a class selector for the update buttons
    $('.update-btn').on('click', function(event) {
        event.preventDefault();

        // Retrieve the product ID associated with the clicked button
        const productId = $(this).data('product-id');

        // Find the corresponding quantity input for the clicked button
        const newQty = $(this).parent().parent().find('.quantity-input').val()

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

    $('.quantity-input').on('change', function() {
        var initialQuantity = this.defaultValue;
        var updateBtn = $(this).parent().parent().find('#update-quantity');
        if (this.value !== initialQuantity) {
            $(updateBtn).addClass('d-block').removeClass('d-none');
        } else {
            $(updateBtn).addClass('d-none').removeClass('d-block');
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