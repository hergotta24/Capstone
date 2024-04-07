document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchForm').addEventListener('submit', function (event) {
        event.preventDefault();
        // Collect form data
        applyFilters()
    });
});


function applyFilters() {
    let searchQuery = $('#search').val()
    if (searchQuery.trim() === '') {
        // Redirect to the home page
        window.location.href = '/';  // Replace '/' with the actual home page URL
        return;  // Stop further execution
    }
    // Get selected filter values
    let selectedFilters = [];
    document.querySelectorAll('input[type="checkbox"]:checked').forEach((checkbox) => {
        selectedFilters.push(checkbox.name);
    });
    if (selectedFilters.length === 0) {
        selectedFilters = ['name', 'store', 'category']
    }

    let filterParams = {
        filters: selectedFilters,
        searchQuery: searchQuery
    }

    // Construct the query string from filterParams
    let queryString = filterParams.filters.map(filter => `filters=${encodeURIComponent(filter)}`).join('&');
queryString += `&searchQuery=${encodeURIComponent(filterParams.searchQuery)}`;

    // Redirect to the URL with query parameters
    window.location.href = '/search/?' + queryString;
}

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
