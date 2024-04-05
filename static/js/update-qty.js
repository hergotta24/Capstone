function checkQuantityChange(input) {
    var initialQuantity = input.defaultValue;
    var updateBtn = input.parentNode.querySelector('.update-btn');

    if (input.value != initialQuantity) {
        updateBtn.style.display = 'inline-block';
    } else {
        updateBtn.style.display = 'none';
    }
}