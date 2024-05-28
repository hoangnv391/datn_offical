// Start: js code for product site
const allColorItem = document.querySelectorAll('.color-item');
const productImage = document.querySelector('.product-image').querySelector('img');
const productPrice = document.querySelector('.price-value');
const addToCartBtn = document.querySelector('#add-to-cart-id');

productPrice.textContent = formatCurrency(productPrice.textContent);

function changeBorder(element) {
    allColorItem.forEach(function(item) {
        item.style.border = '2px solid white';
    });
    element.style.border = '2px solid #002c5f';

    const imgPath = element.getAttribute('data-src');
    const itemPrice = element.getAttribute('data-price');
    const skuId = element.getAttribute('sku-id');

    productImage.src = imgPath;
    productPrice.textContent = formatCurrency(itemPrice);
    addToCartBtn.setAttribute('sku-id', skuId);
};



/* Start: function to change when click an option */
// const productSkus = document.querySelectorAll('.color-item');
// const productImage = document.querySelector('.product-image').querySelector('img');

// productSkus.forEach((item,) => {
//    item.addEventListener(clic)
// });

/* End: function to change when click an option */

// End: js code for product site

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
        url: 'cart/add-to-cart', // đường dẫn tới view xử lý yêu cầu
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