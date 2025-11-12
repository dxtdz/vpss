import http.server
import socketserver
import json
import time
import threading
import os
from datetime import datetime

# Configuration
VNC_PASSWORD = os.getenv("VNC_PASSWORD", "123456")
PORT = int(os.getenv("PORT", "8080"))
START_TIME = time.time()

class VNCServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ultra Light VNC - Render</title>
                <meta charset="UTF-8">
                <style>
                    body {{ margin:20px; font-family:Arial; background:#1a1a1a; color:white; }}
                    .container {{ max-width:600px; margin:0 auto; }}
                    .box {{ background:#2d2d2d; padding:15px; margin:10px 0; border-radius:8px; }}
                    .status {{ color:#4CAF50; font-weight:bold; }}
                    button {{ background:#4CAF50; color:white; border:none; padding:10px 20px; margin:5px; border-radius:5px; cursor:pointer; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Ultra Light VNC - Render</h1>
                    
                    <div class="box">
                        <h3>📊 Server Status</h3>
                        <p>Uptime: <span class="status" id="uptime">0</span>s</p>
                        <p>Platform: <span class="status">Render.com</span></p>
                        <p>Port: <span class="status">{PORT}</span></p>
                    </div>

                    <div class="box">
                        <h3>🛠️ Quick Actions</h3>
                        <button onclick="healthCheck()">Health Check</button>
                        <button onclick="getStats()">Get Stats</button>
                    </div>

                    <div class="box">
                        <h3>📈 Response:</h3>
                        <pre id="response">Click buttons above</pre>
                    </div>
                </div>

                <script>
                    let startTime = Date.now();

                    function updateUptime() {{
                        document.getElementById('uptime').textContent = 
                            Math.floor((Date.now() - startTime) / 1000);
                    }}

                    async function healthCheck() {{
                        try {{
                            const response = await fetch('/health');
                            const data = await response.json();
                            document.getElementById('response').textContent = JSON.stringify(data, null, 2);
                        }} catch (error) {{
                            document.getElementById('response').textContent = 'Error: ' + error;
                        }}
                    }}

                    async function getStats() {{
                        try {{
                            const response = await fetch('/stats');
                            const data = await response.json();
                            document.getElementById('response').textContent = JSON.stringify(data, null, 2);
                        }} catch (error) {{
                            document.getElementById('response').textContent = 'Error: ' + error;
                        }}
                    }}

                    setInterval(updateUptime, 1000);
                    // Auto health check every 2 minutes for uptime
                    setInterval(healthCheck, 120000);
                </script>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "ultra-light-vnc",
                "platform": "render",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": round(time.time() - START_TIME, 2)
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "total_requests": "tracked",
                "platform": "render-free-tier",
                "recommended_uptime_check": "5 minutes",
                "endpoints": ["/", "/health", "/stats"]
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # Reduced logging for better performance
        print(f"{datetime.now().isoformat()} - {self.address_string()} - {format % args}")

print(f"🚀 Starting Ultra Light VNC Server on port {PORT}")
print(f"🔗 Ready for Render.com deployment")
print(f"⏰ Start time: {datetime.now().isoformat()}")

with socketserver.TCPServer(("", PORT), VNCServer) as httpd:
    print(f"✅ Server running at http://0.0.0.0:{PORT}")
    httpd.serve_forever()
