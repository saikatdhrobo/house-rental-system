// script.js

// Log a welcome message when the page loads
document.addEventListener("DOMContentLoaded", () => {
    console.log("Welcome to Kaliakair Rental Solution!");
    applyDynamicEffects();
});

// Function to apply hover effects dynamically (optional example)
function applyDynamicEffects() {
    const buttons = document.querySelectorAll(".btn");

    buttons.forEach((button) => {
        button.addEventListener("mouseover", () => {
            button.style.transform = "scale(1.1)"; // Slight zoom on hover
        });

        button.addEventListener("mouseout", () => {
            button.style.transform = "scale(1)"; // Reset zoom
        });
    });
}

// Function to navigate to different pages
function navigateTo(page) {
    window.location.href = page;
}

// Event listeners for buttons (if you want to avoid inline JS in HTML)
const loginButton = document.querySelector(".btn:first-child");
const registerButton = document.querySelector(".btn:last-child");

if (loginButton && registerButton) {
    loginButton.addEventListener("click", () => navigateTo("login.html"));
    registerButton.addEventListener("click", () => navigateTo("register.html"));
}
