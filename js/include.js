// Lädt HTML-Komponenten automatisch in Elemente mit data-include und führt enthaltene Skripte aus
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

                // Skripte extrahieren und ausführen, da innerHTML sie standardmäßig blockiert
                const scripts = el.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    Array.from(oldScript.attributes).forEach(attr => {
                        newScript.setAttribute(attr.name, attr.value);
                    });
                    newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                });
            })
            .catch(error => console.error(error));
    });
});
