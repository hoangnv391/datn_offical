/* Start: js code for cart site */

// Lấy tất cả các thẻ p có class là "item-price"
const cartItemPriceElements = document.querySelectorAll('.item-price-cart');
const divCastValue = document.querySelector('#cast-value');
const divTotalPayValue = document.querySelector('#total-pay-value');

divCastValue.textContent = formatCurrency(divCastValue.textContent);
divTotalPayValue.textContent = formatCurrency(divTotalPayValue.textContent);

// Lặp qua từng thẻ p và cập nhật nội dung
cartItemPriceElements.forEach(function(element) {
    element.textContent = formatCurrency(element.textContent);
});

$(document).ready(function () {
    $('.quantity-control-btn').click(function () {
        var inputElement = $(this).siblings('.motobike-quantity'); // lấy thẻ input gần nhất có class là motobike-quantity
        var itemContainer = $(this).closest('.item-specification');

        var itemId = inputElement.attr('item-id');
        itemId = parseInt(itemId);
        var currentValue = parseInt(inputElement.val());
        var quantity = 0;

        if ($(this).hasClass('minus')) {
            var newValue = currentValue - 1;
            if (newValue > 0) {
                inputElement.val(newValue);
                quantity = newValue;
            }
            else {
                inputElement.val(0);
                quantity = (newValue >= 0 ? newValue : 0);
                itemContainer.remove();
            }
        } else if ($(this).hasClass('add')) {
            var newValue = currentValue + 1;
            inputElement.val(newValue);
            quantity = newValue;
        }

        var jsonData = {
            'item_id': itemId,
            'quantity': quantity
        }

        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });

        $.ajax({
            url: 'cart/change-quantity', // đường dẫn tới view xử lý yêu cầu
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(jsonData),
            contentType: 'application/json',
            // data: {
            //     'sku-id': "1"
            // },
            success: function(response) {
                // alert(response.message);
                castValue = document.querySelector('#cast-value');
                totalPayValue = document.querySelector('#total-pay-value');
                castValue.textContent = formatCurrency(String(response.cast_value));
                totalPayValue.textContent = formatCurrency(String(response.cast_value));
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + shr.responseText);
            }
        });
    });
});

$(document).ready(function () {
    $('.item-delete').click(function () {
        var inputElement = $(this);// lấy thẻ input gần nhất có class là motobike-quantity
        var itemContainer = $(this).closest('.item-specification');

        var itemId = inputElement.attr('item-id');
        itemId = parseInt(itemId);
        var currentValue = parseInt(inputElement.val());
        var quantity = 0;


        var jsonData = {
            'item_id': itemId,
            'quantity': quantity
        }

        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });

        $.ajax({
            url: 'cart/change-quantity', // đường dẫn tới view xử lý yêu cầu
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(jsonData),
            contentType: 'application/json',
            // data: {
            //     'sku-id': "1"
            // },
            success: function(response) {
                // alert(response.message);
                castValue = document.querySelector('#cast-value');
                totalPayValue = document.querySelector('#total-pay-value');
                castValue.textContent = formatCurrency(String(response.cast_value));
                totalPayValue.textContent = formatCurrency(String(response.cast_value));
                itemContainer.remove();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + shr.responseText);
            }
        });
    });
});

/* End: js code for cart site */