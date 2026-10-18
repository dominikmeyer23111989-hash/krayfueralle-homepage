// Lädt HTML-Komponenten automatisch in Elemente mit data-include
document.addEventListener("DOMContentLoaded", function() {
    const includes = document.querySelectorAll('[data-include]');
    includes.forEach(el => {
        const file = el.getAttribute('data-include');
        fetch(file)
            .then(response => {
                if (response.ok) return response.text();
                throw new Error('Fehler beim Laden der Komponente');
            })
            .then(data => {
                el.innerHTML = data;
            })
            .catch(error => console.error(error));
    });
});
