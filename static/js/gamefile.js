let playerScore = parseInt(document.getElementById("playerScore")?.innerText || 0);
let computerScore = parseInt(document.getElementById("computerScore")?.innerText || 0);

const startBtn = document.getElementById("startBtn");
const gameArea = document.getElementById("gameArea");
const resultText = document.getElementById("result");

const playerScoreEl = document.getElementById("playerScore");
const computerScoreEl = document.getElementById("computerScore");

const clickSound = new Audio("/static/assets/click.wav");

// CANVAS SETUP
const canvas = document.getElementById("gameCanvas");
const ctx = canvas ? canvas.getContext("2d") : null;

// Draw initial state
if (ctx) {
    drawText("Click Start to Play!");
}

function drawText(text) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = "20px Arial";
    ctx.textAlign = "center";
    ctx.fillText(text, canvas.width / 2, canvas.height / 2);
}

// Draw battle
function drawBattle(player, computer, result) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.font = "50px Arial";
    ctx.textAlign = "center";

    const emojis = {
        rock: "🪨",
        paper: "📄",
        scissors: "✂️"
    };

    // Player side
    ctx.fillText(emojis[player], canvas.width * 0.25, canvas.height / 2);

    // VS text
    ctx.font = "20px Arial";
    ctx.fillText("VS", canvas.width * 0.5, canvas.height / 2);

    // Computer side
    ctx.font = "50px Arial";
    ctx.fillText(emojis[computer], canvas.width * 0.75, canvas.height / 2);

    // Result text
    ctx.font = "18px Arial";
    ctx.fillText(result, canvas.width / 2, canvas.height - 20);
}

if (startBtn) {
    startBtn.addEventListener("click", () => {
        gameArea.style.display = "block";
        startBtn.style.display = "none";

        drawText("Make your move!");
    });
}

const choices = document.querySelectorAll(".choice");

choices.forEach(button => {
    button.addEventListener("click", async () => {

        // disable buttons briefly
        toggleButtons(true);

        clickSound.play();

        const playerChoice = button.dataset.choice;
        const computerChoice = getComputerChoice();

        const result = getWinner(playerChoice, computerChoice);

        drawBattle(playerChoice, computerChoice, result);

        resultText.classList.add("fade");
        resultText.innerText = `You: ${playerChoice} | Computer: ${computerChoice} → ${result}`;

        if (result === "You win!") playerScore++;
        if (result === "Computer wins!") computerScore++;

        playerScoreEl.innerText = playerScore;
        computerScoreEl.innerText = computerScore;

        await updateScore();

        checkWinner();

        setTimeout(() => {
            toggleButtons(false);
            resultText.classList.remove("fade");
        }, 800);
    });
});

function toggleButtons(disabled) {
    choices.forEach(btn => btn.disabled = disabled);
}

function getComputerChoice() {
    const options = ["rock", "paper", "scissors"];
    return options[Math.floor(Math.random() * 3)];
}

function getWinner(player, computer) {
    if (player === computer) return "Draw";

    if (
        (player === "rock" && computer === "scissors") ||
        (player === "paper" && computer === "rock") ||
        (player === "scissors" && computer === "paper")
    ) return "You win!";

    return "Computer wins!";
}

async function updateScore() {
    await fetch("/update_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            player_score: playerScore,
            computer_score: computerScore
        })
    });
}

function checkWinner() {
    if (playerScore === 3) {
        alert("🏆 You won the match!");
        resetGame();
    } else if (computerScore === 3) {
        alert("💻 Computer won the match!");
        resetGame();
    }
}

function resetGame() {
    playerScore = 0;
    computerScore = 0;
    playerScoreEl.innerText = 0;
    computerScoreEl.innerText = 0;
    updateScore();
}