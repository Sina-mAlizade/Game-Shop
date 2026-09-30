(function () {
    "use strict";

    var body = document.body;
    var toggleBtn = document.getElementById('themeToggle');

    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
    }
    document.documentElement.classList.remove('dark-mode-init');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            body.classList.toggle('dark-mode');
            var isDark = body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }
})();
