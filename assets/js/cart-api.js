function getCsrfToken() {
    var input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    // اگه فرمی توی صفحه نبود، از کوکی می‌گیریم
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
}

function apiPost(url) {
    return fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() }
    }).then(res => res.json());
}

function updateCartBadge(cartData) {
    var badge = document.querySelector('.cart-count');
    if (badge) badge.textContent = cartData.total_items;
}

// ---------- افزودن به سبد (صفحه‌ی محصول) ----------
document.querySelectorAll('.add-to-cart-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        var gameId = this.dataset.gameId;
        apiPost(`/api/cart/add/${gameId}/`).then(updateCartBadge);
    });
});

// ---------- تغییر تعداد / حذف (صفحه‌ی سبد خرید) ----------
document.querySelectorAll('.increase-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        var itemId = this.dataset.itemId;
        apiPost(`/api/cart/increase/${itemId}/`).then(renderCartPage);
    });
});

document.querySelectorAll('.decrease-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        var itemId = this.dataset.itemId;
        apiPost(`/api/cart/decrease/${itemId}/`).then(renderCartPage);
    });
});

document.querySelectorAll('.remove-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        var itemId = this.dataset.itemId;
        apiPost(`/api/cart/remove/${itemId}/`).then(renderCartPage);
    });
});

function renderCartPage(cartData) {
    updateCartBadge(cartData);

    var container = document.querySelector('.cart-items-container');
    if (!container) return;

    container.innerHTML = '';
    cartData.items.forEach(function (item) {
        container.innerHTML += `
            <div class="cart-item">
                <img src="${item.game.image}" style="width:70px;">
                <span>${item.game.title}</span>
                <button class="decrease-btn" data-item-id="${item.id}">-</button>
                <strong>${item.quantity}</strong>
                <button class="increase-btn" data-item-id="${item.id}">+</button>
                <span>$${item.total_price}</span>
                <button class="remove-btn" data-item-id="${item.id}">حذف</button>
            </div>
        `;
    });

    document.querySelector('.cart-total').textContent = '$' + cartData.total_price;

    // چون دکمه‌های جدید تازه ساخته شدن، دوباره event listener بذار
    attachCartEvents();
}

function attachCartEvents() {
    document.querySelectorAll('.increase-btn').forEach(function (btn) {
        btn.onclick = function () {
            apiPost(`/api/cart/increase/${this.dataset.itemId}/`).then(renderCartPage);
        };
    });
    document.querySelectorAll('.decrease-btn').forEach(function (btn) {
        btn.onclick = function () {
            apiPost(`/api/cart/decrease/${this.dataset.itemId}/`).then(renderCartPage);
        };
    });
    document.querySelectorAll('.remove-btn').forEach(function (btn) {
        btn.onclick = function () {
            apiPost(`/api/cart/remove/${this.dataset.itemId}/`).then(renderCartPage);
        };
    });
}

// ---------- جستجوی زنده (فیلد جستجوی فروشگاه) ----------
var searchInput = document.querySelector('input[name="q"]');
var searchResultsBox = document.getElementById('liveSearchResults');
var searchTimeout;

if (searchInput) {
    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        var query = this.value;

        if (query.length < 2) {
            searchResultsBox.innerHTML = '';
            searchResultsBox.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(function () {
            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(function (games) {
                    searchResultsBox.innerHTML = '';
                    if (games.length === 0) {
                        searchResultsBox.style.display = 'none';
                        return;
                    }
                    games.forEach(function (g) {
                        searchResultsBox.innerHTML += `
                            <a href="/product/${g.id}/" class="live-search-item">
                                <img src="${g.image}" class="live-search-thumb">
                                <span>${g.title}</span>
                            </a>
                        `;
                    });
                    searchResultsBox.style.display = 'block';
                });
        }, 300); // 300ms تاخیر تا هر حرف باعث درخواست جدا نشه
    });
}