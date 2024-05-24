function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function addToCart() {
    var csrftoken = getCookie('csrftoken');
    var sku_id = $('#add-to-cart-id').attr('sku-id');
    var jsonData = {
        'sku_id': sku_id
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });

    console.log(sku_id)
    console.log(typeof(sku_id))

    $.ajax({
        url: 'product/add-to-cart', // đường dẫn tới view xử lý yêu cầu
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify(jsonData),
        contentType: 'application/json',
        // data: {
        //     'sku-id': "1"
        // },
        success: function(response) {
            alert(response.message);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + shr.responseText);
        }
    });
}