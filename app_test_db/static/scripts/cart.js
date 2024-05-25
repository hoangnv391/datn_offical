/* Start: js code for cart site */

// Lấy tất cả các thẻ p có class là "item-price"
const cartItemPriceElements = document.querySelectorAll('.item-price-cart');

// Lặp qua từng thẻ p và cập nhật nội dung
cartItemPriceElements.forEach(function(element) {
    element.textContent = formatCurrency(element.textContent);
});

/* End: js code for cart site */