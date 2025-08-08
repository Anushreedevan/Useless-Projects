document.addEventListener("DOMContentLoaded", function() {
    const progressBar = document.getElementById('progress-fill');
    const loadingScreen = document.getElementById('loading-screen');
    const mainPage = document.getElementById('main-page');

    setTimeout(() => {
        progressBar.style.width = '100%';
    }, 100);

    setTimeout(() => {
        loadingScreen.style.display = 'none';
        mainPage.style.display = 'block';
    }, 3000);
});

async function updateWhistleCount() {
    try {
        const response = await fetch('/get_count');
        const data = await response.json();

        const countLabel = document.getElementById('whistle-count');
        countLabel.textContent = `${data.count} / 3`;

        if (data.count >= 3) {
            document.getElementById('status-message').textContent = 'Cooker is done! Amma\'s voice played.';
            document.getElementById('main-page').style.display = 'none';
            document.getElementById('video-page').style.display = 'flex'; // Show video page
            stopListening();
        }

    } catch (error) {
        console.error('Error fetching count:', error);
        document.getElementById('status-message').textContent = 'Error connecting to backend.';
    }
}

let intervalId;

async function startListening() {
    const statusMessage = document.getElementById('status-message');
    const timerLine = document.querySelector('.timer-line');

    try {
        const response = await fetch('/start_listening');
        const data = await response.json();
        statusMessage.textContent = data.status;

        timerLine.classList.add('spinning');
        intervalId = setInterval(updateWhistleCount, 1000);

    } catch (error) {
        console.error('Error starting backend:', error);
        statusMessage.textContent = 'Error starting backend.';
    }
}

async function stopListening() {
    const statusMessage = document.getElementById('status-message');
    const timerLine = document.querySelector('.timer-line');

    try {
        const response = await fetch('/stop_listening');
        const data = await response.json();
        statusMessage.textContent = data.status;

        timerLine.classList.remove('spinning');
        clearInterval(intervalId);

    } catch (error) {
        console.error('Error stopping backend:', error);
        statusMessage.textContent = 'Error stopping backend.';
    }
}

function goBackToMain() {
    document.getElementById('video-page').style.display = 'none';
    document.getElementById('main-page').style.display = 'block';
    document.getElementById('whistle-count').textContent = '0 / 3'; // Reset counter
    document.getElementById('status-message').textContent = 'Ready to start.';
}

document.getElementById('start-button').addEventListener('click', startListening);
document.getElementById('stop-button').addEventListener('click', stopListening);
document.getElementById('back-to-main').addEventListener('click', goBackToMain);

updateWhistleCount();