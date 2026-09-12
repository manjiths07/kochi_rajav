let botActive = true;

function toggleBot() {
    botActive = !botActive;
    let btn = document.getElementById("toggle-btn");
    if(botActive) {
        btn.innerText = "Deactivate Bot";
        btn.style.backgroundColor = "#f59e0b";
        addLog("Bot activated.");
    } else {
        btn.innerText = "Activate Bot";
        btn.style.backgroundColor = "#10b981";
        addLog("Bot deactivated (Safe zone!).");
    }
}

function addLog(text) {
    let list = document.getElementById("log-list");
    let li = document.createElement("li");
    li.innerText = "[" + new Date().toLocaleTimeString() + "] " + text;
    list.prepend(li);
}

// Check status every 3 seconds
setInterval(() => {
    if (!botActive) return;

    fetch('/check-status')
    .then(response => response.json())
    .then(data => {
        let card = document.getElementById("status-card");
        let text = document.getElementById("status-text");

        if (data.distracted) {
            card.className = "status danger";
            text.innerText = "🚨 DISTRACTED! SLAP INCOMING!";
            addLog("Warning: Distraction detected! Signal sent to Arduino/Face.");
        } else {
            card.className = "status safe";
            text.innerText = "Status: Working Hard 💻";
        }
    });
}, 3000);