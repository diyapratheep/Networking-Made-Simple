# Traffic Simulator - Real Traceroute Backend (Local)

This adds a small Node.js backend that runs the system `traceroute` / `tracert` command and streams hop results to the browser via WebSocket.

Files added:
- `server.js` - Node.js server + WebSocket listener. Also serves static files so you can open `http://localhost:3000/main.html`.
- `package.json` - for installing required packages and running the server.
- `hop_simulator.js` - updated to optionally connect to the WebSocket and animate real traceroute results.

Quick start (Windows PowerShell):

```powershell
npm install
npm start
```

Then open: `http://localhost:3000/main.html` in your browser.

Usage notes
- Check the box "Use real traceroute (local server)" in the Hop Visualization controls, enter a destination IP or hostname, then click "Start Trace".
- The backend will spawn `traceroute` (macOS/Linux) or `tracert` (Windows). The server must run on the same machine where you want to perform traces.
- This server must be run locally (it executes system network commands). Keep it private and do not expose it publicly without adding authentication and rate-limiting.

Security considerations
- The server sanitizes the target to basic hostname/IP characters, but do not expose it to untrusted networks or users.
- For public deployment, add authentication, rate-limiting, and input validation.

If you want, I can also:
- Improve parsing robustness for more traceroute output varieties.
- Add geolocation/ASN lookups for each hop and map visualization.
- Add a toggle to export the raw traceroute output.
