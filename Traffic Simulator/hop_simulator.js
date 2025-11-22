

(function () {
    // Utility DOM references
    const svg = document.getElementById('topologyCanvas');
    const startBtn = document.getElementById('startTraceBtn');
    const stepBtn = document.getElementById('stepTraceBtn');
    const resetBtn = document.getElementById('resetTraceBtn');
    const hopLog = document.getElementById('hopLog');
    const speedRange = document.getElementById('speedRange');

    let pathNodes = []; // nodes with x,y,name,ip
    let pathLinks = []; // links connecting nodes
    let packetDot = null;
    let animation = null;
    let currentSegment = 0;
    let tProgress = 0; // 0..1 along current segment
    let playing = false;
    let speed = 1;

    function clearSvg() {
        while (svg.firstChild) svg.removeChild(svg.firstChild);
    }

    function createSvgNode(x, y, label, cls = '') {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('transform', `translate(${x}, ${y})`);

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('r', 18);
        circle.setAttribute('fill', cls === 'router' ? '#f6ad55' : '#60a5fa');
        circle.setAttribute('stroke', '#111827');
        circle.setAttribute('stroke-width', '1');
        g.appendChild(circle);

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', 0);
        text.setAttribute('y', 5);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-size', '11');
        text.setAttribute('fill', '#0f172a');
        text.textContent = label;
        g.appendChild(text);

        svg.appendChild(g);
        return g;
    }

    function createLink(x1, y1, x2, y2) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', '#94a3b8');
        line.setAttribute('stroke-width', '2');
        svg.appendChild(line);
        return line;
    }

    function createPacketDot(x, y) {
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', x);
        dot.setAttribute('cy', y);
        dot.setAttribute('r', '6');
        dot.setAttribute('fill', '#ef4444');
        dot.setAttribute('opacity', '0.95');
        svg.appendChild(dot);
        return dot;
    }

    function setLog(text) {
        const el = document.createElement('div');
        el.className = 'text-sm text-gray-700 mb-1';
        el.textContent = text;
        hopLog.appendChild(el);
        hopLog.scrollTop = hopLog.scrollHeight;
    }

    // Builds a simple path based on the inputs; simple simulated topology
    function buildPath() {
        // Read inputs from main form
        const localIp = document.getElementById('localIp').value.trim();
        const cidr = parseInt(document.getElementById('cidrPrefix').value.trim(), 10);
        const defaultGw = document.getElementById('defaultGateway').value.trim();
        const destinationIp = document.getElementById('destinationIp').value.trim();

        // Basic validation
        if (!window.isValidIp || !isValidIp(localIp) || !isValidIp(defaultGw) || !isValidIp(destinationIp) || isNaN(cidr)) {
            setLog('Invalid inputs for trace. Please check IPs and CIDR.');
            return null;
        }

        const localLong = window.ipToLong(localIp);
        const destLong = window.ipToLong(destinationIp);
        const mask = window.cidrToLongMask(cidr);
        const localNet = localLong & mask;
        const destNet = destLong & mask;

        const nodes = [];
        const links = [];

        // positions chosen to fit the SVG viewBox
        const hostPos = { x: 80, y: 110 };
        const gwPos = { x: 260, y: 110 };
        const ispPos = { x: 460, y: 70 };
        const destPos = { x: 680, y: 110 };

        // Host node
        nodes.push({ id: 'host', x: hostPos.x, y: hostPos.y, name: 'Host', ip: localIp, type: 'host' });

        if (localNet === destNet) {
            // Destination is local: single gateway not needed
            nodes.push({ id: 'dest', x: destPos.x, y: destPos.y, name: 'Destination', ip: destinationIp, type: 'host' });
            links.push({ from: 0, to: 1, latency: 3 });
        } else {
            // External path: host -> gw -> isp -> dest
            nodes.push({ id: 'gw', x: gwPos.x, y: gwPos.y, name: 'Gateway', ip: defaultGw, type: 'router' });
            nodes.push({ id: 'isp', x: ispPos.x, y: ispPos.y, name: 'ISP-Rtr', ip: '203.0.113.1', type: 'router' });
            nodes.push({ id: 'dest', x: destPos.x, y: destPos.y, name: 'Destination', ip: destinationIp, type: 'host' });

            // latencies are simulated; could be configurable later
            links.push({ from: 0, to: 1, latency: 6 }); // host->gw
            links.push({ from: 1, to: 2, latency: 30 }); // gw->isp
            links.push({ from: 2, to: 3, latency: 50 }); // isp->dest
        }

        return { nodes, links };
    }

    function renderTopology(model) {
        clearSvg();
        pathNodes = model.nodes;
        pathLinks = model.links;

        // Draw links
        for (const link of pathLinks) {
            const a = pathNodes[link.from];
            const b = pathNodes[link.to];
            createLink(a.x, a.y, b.x, b.y);
        }

        // Draw nodes
        pathNodes.forEach(n => createSvgNode(n.x, n.y, `${n.name}\n${n.ip}`, n.type === 'router' ? 'router' : 'host'));

        // Create packet dot at host
        if (packetDot) packetDot.remove();
        const start = pathNodes[0];
        packetDot = createPacketDot(start.x, start.y);

        // initial reset
        currentSegment = 0;
        tProgress = 0;
        playing = false;
        setLog('Topology rendered. Ready to trace.');
    }

    function stepTrace() {
        // Move the simulation forward by one hop (segment)
        if (!pathLinks || pathLinks.length === 0) return;
        if (currentSegment >= pathLinks.length) {
            setLog('Trace complete.');
            return;
        }

        // Jump the packet to the end of the segment immediately
        const link = pathLinks[currentSegment];
        const from = pathNodes[link.from];
        const to = pathNodes[link.to];
        packetDot.setAttribute('cx', to.x);
        packetDot.setAttribute('cy', to.y);

        // Log arrival and simulated latency
        setLog(`Hop ${currentSegment + 1}: ${to.name} (${to.ip}) — ${link.latency} ms`);
        currentSegment += 1;
    }

    function resetTrace() {
        if (!pathNodes || pathNodes.length === 0) return;
        const start = pathNodes[0];
        packetDot.setAttribute('cx', start.x);
        packetDot.setAttribute('cy', start.y);
        currentSegment = 0;
        tProgress = 0;
        playing = false;
        hopLog.innerHTML = '';
        setLog('Trace reset.');
    }

    function animateStep(timestamp) {
        if (!playing) return;
        if (!pathLinks || pathLinks.length === 0) return;
        const seg = pathLinks[currentSegment];
        if (!seg) {
            setLog('Trace finished.');
            playing = false;
            return;
        }

        const from = pathNodes[seg.from];
        const to = pathNodes[seg.to];

        // speedFactor controls how fast tProgress increases
        const speedFactor = Number(speedRange.value) || 1;
        tProgress += 0.007 * speedFactor; // base speed
        if (tProgress >= 1) {
            // arrive at the next node
            packetDot.setAttribute('cx', to.x);
            packetDot.setAttribute('cy', to.y);
            setLog(`Hop ${currentSegment + 1}: ${to.name} (${to.ip}) — ${seg.latency} ms`);
            currentSegment += 1;
            tProgress = 0;

            // If finished
            if (currentSegment >= pathLinks.length) {
                setLog('Trace complete.');
                playing = false;
                return;
            }
        } else {
            // interpolate position
            const x = from.x + (to.x - from.x) * tProgress;
            const y = from.y + (to.y - from.y) * tProgress;
            packetDot.setAttribute('cx', x);
            packetDot.setAttribute('cy', y);
        }

        animation = window.requestAnimationFrame(animateStep);
    }

    // Bind UI
    startBtn.addEventListener('click', () => {
        // Build path from current inputs and render
        hopLog.innerHTML = '';
        const model = buildPath();
        if (!model) return;
        renderTopology(model);
        // start playing
        playing = true;
        animation = window.requestAnimationFrame(animateStep);
    });

    stepBtn.addEventListener('click', () => {
        if (!packetDot || !pathLinks) {
            const model = buildPath();
            if (!model) return;
            renderTopology(model);
        }
        playing = false;
        window.cancelAnimationFrame(animation);
        stepTrace();
    });

    resetBtn.addEventListener('click', () => {
        resetTrace();
    });

    // Allow pressing Enter in destination input to trigger trace
    const destinationInput = document.getElementById('destinationIp');
    destinationInput && destinationInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') startBtn.click();
    });

    // Initialize a default render on script load using current inputs
    document.addEventListener('DOMContentLoaded', () => {
        const model = buildPath();
        if (model) renderTopology(model);
    });

})();
