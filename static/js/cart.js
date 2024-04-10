let coll = document.getElementsByClassName("collapsible");
let i;

for (i = 0; i < coll.length; i++)
{
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        let content = this.nextElementSibling.firstElementChild;
        if (content.style.display === "table") {
            content.style.display = "none";
        } else {
            content.style.display = "table";
        }
    });
}


document.getElementById('cartForm').addEventListener('submit', function (event) {
    event.preventDefault();

    // Collect form data
    const cartData = {
        name: this.elements.name.value,
        card: this.elements.card.value,
        expiration: this.elements.expiration.value,
        back_number: this.elements.back_number.value,
    };

    // Send form data using fetch post request
    fetch('/cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Function to get CSRF token
        },
        body: JSON.stringify(cartData)
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
