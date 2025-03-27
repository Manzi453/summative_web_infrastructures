// Theme Toggle
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Check for saved theme preference
const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    body.classList.add(currentTheme);
    updateThemeButton();
}

themeToggle.addEventListener('click', () => {
    if (body.classList.contains('light-theme')) {
        body.classList.replace('light-theme', 'dark-theme');
        localStorage.setItem('theme', 'dark-theme');
    } else {
        body.classList.replace('dark-theme', 'light-theme');
        localStorage.setItem('theme', 'light-theme');
    }
    updateThemeButton();
});

function updateThemeButton() {
    if (body.classList.contains('dark-theme')) {
        themeToggle.textContent = '☀️ Light Mode';
    } else {
        themeToggle.textContent = '🌙 Dark Mode';
    }
}

// Country Functions
async function fetchCountry() {
    const name = document.getElementById("country-input").value.trim();
    if (!name) return;

    try {
        const response = await fetch(`/country/${name}`);
        const data = await response.json();
        displayResult(data);
    } catch (error) {
        document.getElementById("result").innerHTML = "❌ Failed to fetch data.";
    }
}

async function fetchRandomCountry() {
    try {
        const response = await fetch("/random");
        const data = await response.json();
        displayResult(data);
    } catch (error) {
        document.getElementById("result").innerHTML = "❌ Failed to load random country.";
    }
}

function displayResult(data) {
    const resultDiv = document.getElementById("result");
    if (data.error) {
        resultDiv.innerHTML = `❌ ${data.error}`;
    } else {
        resultDiv.innerHTML = `
            <h2>${data.country}</h2>
            ${data.flag ? `<img src="${data.flag}" alt="Flag" class="country-flag">` : ''}
            <p><strong>Capital:</strong> ${data.capital}</p>
            <p><strong>Population:</strong> ${data.population}</p>
            <p><strong>Languages:</strong> ${data.languages}</p>
        `;
    }
}

// Load random country on startup
window.onload = fetchRandomCountry;
