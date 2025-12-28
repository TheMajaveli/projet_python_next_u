/**
 * Gestion du thème Dark Mode
 */

(function() {
    'use strict';

    // Récupérer le thème sauvegardé ou utiliser le thème par défaut
    const getTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        return savedTheme || 'light';
    };

    // Appliquer le thème
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateToggleButton(theme);
    };

    // Mettre à jour le bouton toggle
    const updateToggleButton = (theme) => {
        const themeIcon = document.getElementById('theme-icon');
        const themeText = document.getElementById('theme-text');
        
        if (theme === 'dark') {
            if (themeIcon) themeIcon.textContent = '☀️';
            if (themeText) themeText.textContent = 'Mode clair';
            document.getElementById('theme-toggle')?.setAttribute('aria-label', 'Passer en mode clair');
        } else {
            if (themeIcon) themeIcon.textContent = '🌙';
            if (themeText) themeText.textContent = 'Mode sombre';
            document.getElementById('theme-toggle')?.setAttribute('aria-label', 'Passer en mode sombre');
        }
    };

    // Toggle du thème
    const toggleTheme = () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    };

    // Initialisation au chargement de la page
    document.addEventListener('DOMContentLoaded', () => {
        const theme = getTheme();
        setTheme(theme);

        // Ajouter l'événement au bouton toggle
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleTheme);
        }
    });

    // Exposer la fonction toggle pour utilisation globale
    window.toggleTheme = toggleTheme;
})();

