function updateTime() {
    const now = new Date();
    document.getElementById("currentTime").textContent =
        now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
setInterval(updateTime, 60000);
updateTime();

function showAlert(text) {
    const el = document.getElementById("alert");
    el.textContent = text;
    el.classList.add("show");
    setTimeout(() => el.classList.remove("show"), 3000);
}

function addMessage(msg) {
    const list = document.getElementById("messagesList");

    const div = document.createElement("div");
    div.className = "message-item";
    div.innerHTML = `
        <b>${msg.sender}</b> (${msg.time})<br>
        ${msg.text}
    `;
    list.prepend(div);
}

async function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();
    if (!text) return;

    await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    input.value = "";
    showAlert("✓ Sent");
    loadMessages();
}

async function sendSOS() {
    await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            text: "🆘 EMERGENCY",
            priority: "critical",
            broadcast: true
        })
    });

    showAlert("🚨 SOS SENT");
    document.getElementById("messagesView").classList.add("active");
    loadMessages();
}

async function loadMessages() {
    const res = await fetch("/messages");
    const data = await res.json();

    const list = document.getElementById("messagesList");
    list.innerHTML = "";

    data.messages.forEach(addMessage);
}

setInterval(loadMessages, 3000);
loadMessages();