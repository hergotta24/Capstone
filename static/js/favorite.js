document.addEventListener('DOMContentLoaded', function () {
    const categoriesContainer = document.getElementById('categories-container');
    const leftArrow = document.getElementById('left-arrow');
    const rightArrow = document.getElementById('right-arrow');

    leftArrow.addEventListener('click', function () {
        categoriesContainer.scrollLeft -= 100; // Adjust scroll speed as needed
    });

    rightArrow.addEventListener('click', function () {
        categoriesContainer.scrollLeft += 100; // Adjust scroll speed as needed
    });

    // Optionally, you can add keyboard support for arrow keys
    document.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowLeft') {
            categoriesContainer.scrollLeft -= 100; // Adjust scroll speed as needed
        } else if (event.key === 'ArrowRight') {
            categoriesContainer.scrollLeft += 100; // Adjust scroll speed as needed
        }
    });
});
