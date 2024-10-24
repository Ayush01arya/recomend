let timerId;
let timeLeft = 60;

// Start the timer
function startTimer() {
    updateTimerDisplay();
    timerId = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 10) {
            document.getElementById('timer').classList.add('blink'); // Add blinking effect
        }
        if (timeLeft <= 0) {
            clearInterval(timerId);
            submitQuiz(); // Automatically submit quiz when time is up
        }
    }, 1000);
}

// Update the timer display
function updateTimerDisplay() {
    const timerElement = document.getElementById('timer');
    timerElement.innerText = `Time Left: ${timeLeft} seconds`;
}

// Start the timer when the page loads
window.onload = startTimer;

const quizForm = document.getElementById("quizForm");

quizForm.addEventListener("submit", (e) => {
    e.preventDefault(); // Prevent default form submission
    submitQuiz(); // Call the submitQuiz function
});

function submitQuiz() {
    clearInterval(timerId); // Stop the timer
    const spinner = document.getElementById('spinner');
    spinner.style.display = 'block'; // Show the spinner

    const answers = {};
    const questions = document.querySelectorAll('.question'); // Select all questions

    // Collect answers
    questions.forEach((question) => {
        const questionId = question.id; // e.g., "q1"
        const selectedOption = question.querySelector('input[type="radio"]:checked');
        if (selectedOption) {
            answers[questionId] = selectedOption.value;
        }
    });

    // Send answers to the backend
    fetch('https://recomend-t26j.vercel.app/submit', {  // Ensure URL matches Flask route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(answers) // Sending answers directly
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        spinner.style.display = 'none'; // Hide spinner
        quizForm.style.display = 'none'; // Hide quiz

        // Show result in a styled way
        const resultContainer = document.getElementById('resultContainer');
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerText = `🎉 Congratulations! Your recommended career is: ${data.recommendation} 🎉`; // Match key with Flask response
        resultContainer.style.display = 'block'; // Show result container
    })
    .catch(error => {
        console.error('Error:', error);
        spinner.style.display = 'none'; // Hide spinner
        alert('An error occurred. Please try again.'); // Show error message
    });
}
