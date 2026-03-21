<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>Emergency Mesh</title>
<link rel="stylesheet" href="/style.css">
</head>

<body>
<div class="phone-frame">

    <div class="status-bar">
        <span id="currentTime">--:--</span>
        <div>📶 4G 🔋 85%</div>
    </div>

    <div class="header">
        <h1>Emergency Dashboard</h1>
        <div id="nodeCount"></div>
    </div>

    <div id="homeView">
        <button class="sos-button" onclick="sendSOS()">SOS</button>
    </div>

    <div id="messagesView" class="messages-view">
        <h2>Messages</h2>
        <div id="messagesList"></div>
    </div>

    <div class="message-section">
        <input id="messageInput" placeholder="Type message...">
        <button onclick="sendMessage()">▶</button>
    </div>

</div>

<div id="alert" class="alert"></div>

<script src="/app.js"></script>
</body>
</html>
