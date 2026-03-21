import http.server
import socketserver
import json
import uuid
import time
from datetime import datetime

from mesh_simulator import MeshNetwork, MeshNode, EMTPMessage, Priority, Location

# ================== SETUP NETWORK ==================
network = MeshNetwork()

nodes = {
    "Node_You": MeshNode("Node_You", Location(16.4322, 102.8236)),
    "Node_A": MeshNode("Node_A"),
    "Node_B": MeshNode("Node_B"),
    "Node_C": MeshNode("Node_C"),
    "Node_D": MeshNode("Node_D"),
    "Node_E": MeshNode("Node_E"),
}

for n in nodes.values():
    network.add_node(n)

network.connect_nodes("Node_You", "Node_A")
network.connect_nodes("Node_You", "Node_C")
network.connect_nodes("Node_A", "Node_B")
network.connect_nodes("Node_B", "Node_E")
network.connect_nodes("Node_C", "Node_D")
network.connect_nodes("Node_D", "Node_E")


# ================== HTTP HANDLER ==================
class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_file("index.html", "text/html")

        elif self.path == "/style.css":
            self.send_file("style.css", "text/css")

        elif self.path == "/app.js":
            self.send_file("app.js", "application/javascript")

        elif self.path == "/messages":
            messages = []

            # ✅ FIX: แสดงทุก message + รวมของตัวเองด้วย
            for node in nodes.values():
                for msg in node.received_messages:
                    messages.append({
                        "sender": msg.source_id,
                        "text": msg.payload,
                        "time": datetime.fromtimestamp(msg.timestamp).strftime("%H:%M"),
                        "priority": msg.priority.name.lower(),
                        "path": " → ".join(msg.forwarding_path),
                        "hops": msg.hop_count
                    })

            self.send_json({
                "messages": messages,
                "node_count": len(nodes)
            })

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/send":
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))

            message = EMTPMessage(
                message_id=str(uuid.uuid4()),
                source_id="Node_You",
                destination_id="BROADCAST" if data.get("broadcast") else "Node_E",
                priority=Priority[data.get("priority", "normal").upper()],
                payload=data["text"],
                location=nodes["Node_You"].location
            )

            network.send_message(message)
            time.sleep(0.5)

            self.send_json({"status": "ok"})

        else:
            self.send_error(404)

    # ================== HELPERS ==================
    def send_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, f"File not found: {path}")

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, *args):
        pass


# ================== RUN SERVER ==================
PORT = 8081  # 🔥 เปลี่ยนเป็น 8081 กัน port ชน

# กัน error port ซ้ำ
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 Server running: http://localhost:{PORT}")
    httpd.serve_forever()