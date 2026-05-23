const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-toggle-icon');
const themeText = document.getElementById('theme-toggle-text');

function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('theme', theme);

    if (!themeIcon || !themeText) {
        return;
    }

    if (theme === 'dark') {
        themeIcon.className = 'fas fa-sun me-1';
        themeText.textContent = 'Modo claro';
    } else {
        themeIcon.className = 'fas fa-moon me-1';
        themeText.textContent = 'Modo escuro';
    }
}

const savedTheme = localStorage.getItem('theme') || 'dark';
setTheme(savedTheme);

themeToggle?.addEventListener('click', () => {
    const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
});
