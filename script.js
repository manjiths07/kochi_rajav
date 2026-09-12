

const dialogues = [
    "Nee enne marannu... pakshe njan ente 4th semester back-um vechu ninne snehichilla.",
    "Evideya sahodara sradha? Aarum illatha lokathu njanum ente oru glass chayam mathrame ullu.",
    "Rathri 3 mani vare reels kandu koovumpol, orkkuka: Oru chaya glass-inte shaapam ninakku kittum.",
    "Nee ippo code cheyyunnillennu ente thengola kannukal kondu njan kandirikkunnu.",
    "Enikku maranamilla, pakshe ninte laziness kandu njan ippo potti theerum!",
    "Oru 10 rupakkulla chaya vaangikodukkan ulla manasillede ninakku?"
];

const avatars = ["☕", "🥺", "💀", "💔", "😭"];

function triggerMelodrama() {
    const randomDialogue = dialogues[Math.floor(Math.random() * dialogues.length)];
    const randomAvatar = avatars[Math.floor(Math.random() * avatars.length)];
    
    document.getElementById("dialogue-box").innerText = `"${randomDialogue}"`;
    document.getElementById("avatar").innerText = randomAvatar;
}

function feedChaya() {
    document.getElementById("dialogue-box").innerText = `"Aha! ippo oru sivasankaran chaya kudi kittiya oru aavesham vanille? Poyirunnu work cheyyada!"`;
    document.getElementById("avatar").innerText = "😎";
}