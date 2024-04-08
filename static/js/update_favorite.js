$(document).ready(function () {
    $('.js-favorite').click(function (e) {
        var favId = $(this).data('productid');
        if ($(this).hasClass('fa-regular')) {
            e.preventDefault()
            fetch('/addFavorite/', {
                method: 'POST',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
                },
                body: JSON.stringify({'favorite_id': favId})
            })
                .then(response => {
                    // Handle response
                    if (response.ok) {
                        console.log('Changes confirmed successfully');
                        $(this).removeClass('fa-regular').addClass('fa-solid');
                    } else {
                        console.error('Error after successful return confirming changes:', response.statusText);
                    }
                })
                .catch(error => {
                    console.error('Error coming back from server', error);
                    // Optionally, display an error message to the user
                });

        } else {
            e.preventDefault()
            fetch('/removeFavorite/', {
                method: 'POST',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
                },
                body: JSON.stringify({'favorite_id': favId})
            })
                .then(response => {
                    // Handle response
                    if (response.ok) {
                        // Successful response
                        console.log('Changes confirmed successfully');
                        $(this).addClass('fa-regular').removeClass('fa-solid');

                    } else {
                        // Error handling
                        console.error('Error confirming changes:', response.statusText);
                    }
                })
                .catch(error => {
                    console.error('Error confirming changes:', error);
                });
        }
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
