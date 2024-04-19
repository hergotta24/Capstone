let name = ""
let description

function setEditable() {
    let confirmBtn = document.getElementById('confirm');
    let cancelBtn = document.getElementById('cancel');
    let logoBtn = document.getElementById('logoBtn');
    let bannerBtn = document.getElementById('bannerBtn');
    let storeName = document.getElementById('storeName');
    let storeDescription = document.getElementById('storeDescription');

    let editBtn = document.getElementById('edit');
    let editBtnContainer = document.getElementById('editLogoBtnContainer');
    storeName.removeAttribute('readonly');
    storeDescription.removeAttribute('readonly');
    confirmBtn.removeAttribute('hidden');
    confirmBtn.removeAttribute('disabled');
    cancelBtn.removeAttribute('hidden');
    cancelBtn.removeAttribute('disabled');
    logoBtn.classList.remove('invisible');
    logoBtn.classList.remove('disabled');
    bannerBtn.classList.remove('invisible');
    bannerBtn.classList.remove('disabled');
    editBtn.classList.add('d-none');
    editBtn.classList.add('disabled');
    editBtnContainer.classList.remove('d-none');
    editBtnContainer.classList.add('d-block');

    name = document.getElementById('storeName').value
    description = document.getElementById('storeDescription').value
}

function cancelEditable() {
    let confirmBtn = document.getElementById('confirm')
    let cancelBtn = document.getElementById('cancel')
    let logoBtn = document.getElementById('logoBtn')
    let bannerBtn = document.getElementById('bannerBtn')
    let storeName = document.getElementById('storeName')
    let storeDescription = document.getElementById('storeDescription');
    let editBtn = document.getElementById('edit')
    storeName.setAttribute('readonly', 'true')
    storeDescription.setAttribute('readonly', 'true')
    confirmBtn.setAttribute('hidden', 'true')
    confirmBtn.setAttribute('disabled', 'true')
    cancelBtn.setAttribute('hidden', 'true')
    cancelBtn.setAttribute('disabled', 'true')
    logoBtn.classList.add('invisible')
    logoBtn.classList.add('disabled')
    bannerBtn.classList.add('invisible')
    bannerBtn.classList.add('disabled')
    editBtn.classList.remove('d-none')
    editBtn.classList.remove('disabled')

    document.getElementById('logoInput').value = '';
    document.getElementById('storeName').value = name;
    document.getElementById('storeDescription').value = description;

}

$(document).ready(function () {
    $('#bannerInput').change(function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                $('#bannerDisplay').attr('src', e.target.result);
            };

            reader.readAsDataURL(file);
        } else {
            return
        }
    });

    $('#logoInput').change(function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                $('#logoDisplay').attr('src', e.target.result);
            };

            reader.readAsDataURL(file);
        } else {
            return
        }
    });

    $('#confirm').click(function (e) {
        e.preventDefault(); // Prevent default form submission

        // Gather data from elements
        var storeName = $('#storeName').val();
        var storeDescription = $('#storeDescription').text(); // Use .text() for contenteditable div
        var bannerInput = $('#bannerInput')[0].files[0];
        var logoInput = $('#logoInput')[0].files[0];

        // Create FormData object to send files along with other data
        var formData = new FormData();
        formData.append('storeName', storeName);
        formData.append('storeDescription', storeDescription);
        formData.append('bannerInput', bannerInput);
        formData.append('logoInput', logoInput);

        // Make POST request using Fetch API
        fetch('/storefront/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
            },
            body: formData
        })
            .then(response => {
                // Handle response
                if (response.ok) {
                    // Successful response
                    console.log('Changes confirmed successfully');
                    // Optionally, redirect or show a success message
                } else {
                    // Error handling
                    console.error('Error confirming changes:', response.statusText);
                    // Optionally, display an error message to the user
                }
            })
            .catch(error => {
                console.error('Error confirming changes:', error);
                // Optionally, display an error message to the user
            });
    });

    $('.js-remove').click(function (e) {
        const removeId = $(this).data('productid');

        e.preventDefault()
        fetch('/removeProduct/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
            },
            body: JSON.stringify({'remove_id': removeId})
        })
            .then(response => {
                // Handle response
                if (response.ok) {
                    location.reload();
                    console.log('Changes confirmed successfully');
                } else {
                    console.error('Error after successful return confirming changes:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error coming back from server', error);
                // Optionally, display an error message to the user
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


