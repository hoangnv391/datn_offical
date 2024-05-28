function formatCurrency(value) {
    // Loại bỏ ký tự đồng Việt Nam (₫) và chuyển đổi chuỗi thành số
    value = parseInt(value.replace(/₫/g, ''));
    // Định dạng số tiền và thêm ký tự đồng Việt Nam (₫) vào cuối
    return value.toLocaleString('vi-VN') + '₫';
};

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

