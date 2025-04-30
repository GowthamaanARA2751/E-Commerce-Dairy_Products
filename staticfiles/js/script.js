$('.plus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var eml = $(this).closest('.cart-item').find('.quantity');  // ✅ Ensure correct element

    console.log('Button clicked! PID:', id);

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: { prod_id: id },
        success: function (data) {
            console.log("Response:", data);
            
            if (data.quantity !== undefined) {
                eml.text(data.quantity);  // ✅ Update quantity text
                $('#amount').text(data.amount);  // ✅ Update amount
                $('#totalamount').text(data.totalamount);  // ✅ Update total amount
            } else {
                console.log("Invalid response format:", data);
            }
        },
        error: function (xhr, status, error) {
            console.log("AJAX Error:", error);
        }
    });
});

$('.minus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var eml = $(this).closest('.cart-item').find('.quantity');  // ✅ Ensure correct element

    console.log('Button clicked! PID:', id);

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: { prod_id: id },
        success: function (data) {
            console.log("Response:", data);
            
            if (data.quantity !== undefined) {
                eml.text(data.quantity);  // ✅ Update quantity text
                $('#amount').text(data.amount);  // ✅ Update amount
                $('#totalamount').text(data.totalamount);  // ✅ Update total amount
            } else {
                console.log("Invalid response format:", data);
            }
        },
        error: function (xhr, status, error) {
            console.log("AJAX Error:", error);
        }
    });
});


$('.remove-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var eml = this

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: { prod_id: id },
        success: function (data) {
            console.log("Response:", data);
            
            if (data.quantity !== undefined) {
                $('#amount').text(data.amount);  // ✅ Update amount
                $('#totalamount').text(data.totalamount);  // ✅ Update total amount
                eml.parentNode.parentNode.parentNode.parentNode.remove()
            } else {
                console.log("Invalid response format:", data);
            }
        },
    });
});

$('.plus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();
    var thisButton = $(this);
    $.ajax({
        type: 'GET',
        url: '/pluswishlist',
        data: {
            prod_id: id
        },
        success: function (data) {
            thisButton.removeClass('plus-wishlist btn-success').addClass('minus-wishlist btn-danger');
            thisButton.html('<i class="fas fa-heart fa-lg"></i>');
        }
    })
});



$(document).on('click', '.minus-wishlist', function () {
    var id = $(this).attr("pid").toString();
    var thisButton = $(this);
    $.ajax({
        type: 'GET',
        url: '/minuswishlist',
        data: {
            prod_id: id
        },
        success: function (data) {
            thisButton.removeClass('minus-wishlist btn-danger').addClass('plus-wishlist btn-success');
            thisButton.html('<i class="fas fa-heart fa-lg"></i>');
        }
    })
});