
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





let imagesArray = []
let imgNum = 0;
let max = 1;

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

function addImage() {
    imgNum++
    if (imgNum === 6) {
        max = 0;
        $('#addSlide').remove()
        $('#addDemo').remove()
    }
    let newImage = document.getElementById('imageInput').files[0];
    imagesArray.push(newImage);
    let imageURL = URL.createObjectURL(newImage);
    let img = $('<img src="" class="col-12" alt="image" style="object-fit: cover; aspect-ratio: 1/1; max-height: 500px;">');
    img.attr('src', imageURL);
    let newSlide = $('<div class="mySlides d-flex col-12 justify-content-center align-content-center"></div>');
    let div = $('<div class="numbertext" style="left:0"><span class="slideNum"></span> / <span class="slideSize"></span></div>')
    div.children('.slideNum').text(imgNum)
    div.children('.slideSize').text(imagesArray.length + max)
    newSlide.append(div)
    newSlide.append(img)

    $('#slideContainer').prepend(newSlide)
    newSlide.addClass("d-none")
    $('.slideSize').each(function () {
        $(this).text(imagesArray.length + max)
    })
    slideIndex = 1;

    let newDemo = $('<div class="col-2 d-flex" style="aspect-ratio: 1/1;object-fit: cover;">\n' +
        '                                <img class="demo cursor" src="" style="max-height: 500px; width:100%; object-fit: cover;"\n' +
        '                                     onclick="currentSlide(1)" alt="image">\n' +
        '                            </div>')
    newDemo.children(".demo").attr('src', imageURL)
    $('#demoContainer').prepend(newDemo)

    document.getElementById('imageInput').value = ''


    showSlides(slideIndex)
}


function showSlides(n) {
    console.log("it's working")
    let slides = document.getElementsByClassName("mySlides");
    //let dots = document.getElementsByClassName("demo");
    //let captionText = document.getElementById("caption");
    if (n > slides.length) {
        slideIndex = 1
        n = 1
    }
    if (n < 1) {
        slideIndex = slides.length
        n = slides.length
    }
    let count = 1
    $('.mySlides').each(function () {
        if(count != n){
            $(this).addClass("d-none").removeClass('d-flex')
        }else{
            $(this).removeClass('d-none').addClass('d-flex')
        }
        count++
    })

    count = 1
    $('.demo').each(function () {
        $(this).attr('onclick', "currentSlide(" + count + ")")
        count++
    })
}