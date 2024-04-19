$(document).ready(function () {
    $('#addShippingDetails').submit(function (event) {
        event.preventDefault();

        // Collect form data
        const formData = $(this).serialize();

        // Send data to server
        fetch('/add-shipping-details/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Changed content type
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData // Sending form data directly
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle response from server
                if (data.error) {
                    console.error('Error:', data.error);
                } else {
                    console.log('Success:', data.message);
                    if (data.buyNowButton){
                        var buttonContainer = $('#buy-now');
                        var buyNowButtonHtml = data.buyNowButton;
                        $(buttonContainer).html(buyNowButtonHtml);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error.message);
            });
    });

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
});

