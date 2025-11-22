#!/bin/bash
# install_traffic_light.sh

echo "🚦 Traffic Light Latency Monitor - Installation"
echo "=============================================="

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "📦 Making scripts executable..."
chmod +x traffic_light.py
chmod +x test_traffic_light.py
chmod +x scenarios.py

echo "✅ Installation complete!"
echo ""
echo "Quick Start:"
echo "  ./traffic_light.py                    # Single check"
echo "  ./traffic_light.py --continuous       # Continuous monitoring"
echo "  ./traffic_light.py --help             # Show all options"
echo ""
echo "Testing:"
echo "  python3 test_traffic_light.py         # Run unit tests"
echo "  python3 scenarios.py                  # See real-world examples"