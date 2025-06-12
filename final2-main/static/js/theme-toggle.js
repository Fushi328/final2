// Theme toggle logic for dark/light mode
(function() {
    const THEME_KEY = 'site-theme';
    const darkClass = 'dark-mode';
    const lightClass = 'light-mode';
    
    function setTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        document.body.classList.remove(darkClass, lightClass);
        document.body.classList.add(theme === 'dark' ? darkClass : lightClass);
    }

    function getSavedTheme() {
        return localStorage.getItem(THEME_KEY) || 'dark';
    }

    document.addEventListener('DOMContentLoaded', function() {
        const toggleBtn = document.getElementById('theme-toggle-btn');
        if (!toggleBtn) return;
        const savedTheme = getSavedTheme();
        setTheme(savedTheme);
        toggleBtn.checked = savedTheme === 'dark';
        toggleBtn.addEventListener('change', function() {
            setTheme(toggleBtn.checked ? 'dark' : 'light');
        });
    });
})();
