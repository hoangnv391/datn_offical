function formatCurrency(value) {
    // Loại bỏ ký tự đồng Việt Nam (₫) và chuyển đổi chuỗi thành số
    value = parseInt(value.replace(/₫/g, ''));
    // Định dạng số tiền và thêm ký tự đồng Việt Nam (₫) vào cuối
    return value.toLocaleString('vi-VN') + '₫';
}

// Lấy tất cả các thẻ p có class là "item-price"
const priceElements = document.querySelectorAll('.item-price');

// Lặp qua từng thẻ p và cập nhật nội dung
priceElements.forEach(function(element) {
    element.textContent = formatCurrency(element.textContent);
});

const imageItems = document.querySelectorAll('.item-option');

imageItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        const imagePath = item.getAttribute('data-src');
        const correspondingDisplayImage = item.closest('.product-item').querySelector('.item-image img');
        correspondingDisplayImage.src = imagePath;

        const itemOption = item.getAttribute('data-option');
        const correspondingDisplayOption = item.closest('.product-item').querySelector('.item-text small');
        correspondingDisplayOption.innerHTML = itemOption;

        const itemPrice = item.getAttribute('data-price');
        const correspondingDisplayPrice = item.closest('.product-item').querySelector('p.item-price');
        correspondingDisplayPrice.innerHTML = formatCurrency(itemPrice);
    });
});

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
}



/* Start: function to change when click an option */
// const productSkus = document.querySelectorAll('.color-item');
// const productImage = document.querySelector('.product-image').querySelector('img');

// productSkus.forEach((item,) => {
//    item.addEventListener(clic)
// });

/* End: function to change when click an option */

// End: js code for product site