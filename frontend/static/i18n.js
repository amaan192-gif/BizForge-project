// Basic i18n structure
const translations = {
    en: {
        title: "Build Your Brand with AI",
        get_started: "Get Started",
        brand_names: "Brand Names",
        logo_generator: "Logo Generator",
        marketing_content: "Marketing Content",
        design_system: "Design System",
        explore: "Explore"
    },
    // Add more languages here
};

let currentLang = 'en';

function setLanguage(lang) {
    currentLang = lang;
    updateUI();
}

function updateUI() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = translations[currentLang][key] || key;
    });
}

document.addEventListener('DOMContentLoaded', updateUI);
