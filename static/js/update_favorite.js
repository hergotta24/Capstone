console.log('favorite id is: ' + $('#favorite').val() + '.')
$('#favorite').change(function (e)
{
    if($('#favorite').is(':checked'))
    {
        e.preventDefault()
        $.ajax({
            method:"POST",
            url:'/addFavorite/',
            headers: {'X-CSRFToken': getCookie("csrftoken")},
            data: JSON.stringify({'favorite_id': $('#favorite').val()})
    });
    }
    else
    {
        e.preventDefault()
        $.ajax({
            method:"POST",
            url:'/removeFavorite/',
            headers: {'X-CSRFToken': getCookie("csrftoken")},
            data: JSON.stringify({'favorite_id': $('#favorite').val()})
    });
    }
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
