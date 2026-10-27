// 1. HTML-Komponenten automatisch in Elemente mit data-include laden
document.addEventListener("DOMContentLoaded", function() {
    const includes = document.querySelectorAll('[data-include]');
    includes.forEach(el => {
        const file = el.getAttribute('data-include');
        fetch(file)
            .then(response => {
                if (response.ok) return response.text();
                throw new Error('Fehler beim Laden der Komponente: ' + file);
            })
            .then(data => {
                el.innerHTML = data;
            })
            .catch(error => console.error(error));
    });
});

// 2. Globaler Event-Listener für das mobile Burger-Menü
// Da dieser Code in der festen include.js liegt, wird er vom Browser problemlos ausgeführt
document.addEventListener('click', function(e) {
    const toggleBtn = e.target.closest('#navToggle');
    const navMenu = document.getElementById('navMenu');

    if (!navMenu) return;

    if (toggleBtn) {
        e.preventDefault();
        e.stopPropagation();
        navMenu.classList.toggle('active');
    } else if (navMenu.classList.contains('active') && !navMenu.contains(e.target)) {
        navMenu.classList.remove('active');
    }
});
