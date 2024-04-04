$(document).ready(function() {
    var form = $('#addShippingDetails');
    var button = form.find('button[type="submit"]');
    var inputs = form.find('input[type="text"], input[type="email"], select');

    function checkForShippingInformation() {
        var filled = true;
        inputs.each(function() {
            if ($(this).prop('required') && !$(this).val().trim()) {
                filled = false;
                return false; // exit loop early
            }
        });
        return filled;
    }

    function updateButtonText() {
        if (checkForShippingInformation()) {
            button.text('Shipping Details Added').removeClass('js-add-shipping-details');
        } else {
            button.text('Add Shipping Details').addClass('js-add-shipping-details');
        }
    }

    // Check on page load
    updateButtonText();

    // Check again on input change
    form.on('input', function() {
        updateButtonText();
    });
});