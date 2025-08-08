document.addEventListener("DOMContentLoaded", function() {
    const progressBar = document.getElementById('progress-fill');
    const loadingScreen = document.getElementById('loading-screen');
    const mainPage = document.getElementById('main-page');

    // Start the loading animation
    setTimeout(() => {
        progressBar.style.width = '100%';
    }, 100);

    // After the animation finishes, hide the loading screen and show the main page
    setTimeout(() => {
        loadingScreen.style.display = 'none';
        mainPage.style.display = 'block';
    }, 3000); // 3000ms = 3 seconds
});