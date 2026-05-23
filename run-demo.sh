#!/bin/bash
# ============================================================
# Smart Drafting Engine - Demo Launcher
# Beauty Contest — 26 Mei 2026
#
# Cara pakai: ./run-demo.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Smart Drafting Engine — POC Demo                      ║"
echo "║  Beauty Contest — 26 Mei 2026                           ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Starting services...                                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Groq API Key for AI features
if [ -z "$GROQ_API_KEY" ]; then
    echo "  ⚠️  GROQ_API_KEY not set. AI features disabled."
    echo "  To enable AI: export GROQ_API_KEY=\"your-key-from-console.groq.com\""
    echo ""
else
    echo "  ✅ GROQ_API_KEY detected. AI features enabled."
    echo ""
fi

# Kill any existing processes on port 8500
lsof -ti:8500 | xargs kill -9 2>/dev/null
sleep 1

# Activate virtual environment
source venv/bin/activate

# Start Backend
echo "[1/2] Starting Python OCR Backend on port 8500..."
python3 backend/app.py &
BACKEND_PID=$!
sleep 2

# Check backend health
HEALTH=$(curl -s http://localhost:8500/health 2>/dev/null)
if echo "$HEALTH" | grep -q "ok"; then
    echo "      ✅ Backend running (PID: $BACKEND_PID)"
else
    echo "      ❌ Backend failed to start!"
    echo "      Log: check terminal output"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start Electron Frontend
echo "[2/2] Starting Electron Desktop App..."
cd "$SCRIPT_DIR/frontend"
npx electron . &
ELECTRON_PID=$!
cd "$SCRIPT_DIR"
sleep 2
echo "      ✅ Electron app launched (PID: $ELECTRON_PID)"

echo ""
echo "══════════════════════════════════════════════════════════"
echo "  Demo is running!"
echo ""
echo "  Backend:  http://localhost:8500"
echo "  Frontend: Electron window"
echo ""
echo "  Sample docs: sample-docs/"
echo "    • sample_invoice.png"
echo "    • sample_bill_of_lading.png"
echo "    • sample_invoice_scan.jpg"
echo ""
echo "  Press Ctrl+C to stop all services"
echo "══════════════════════════════════════════════════════════"
echo ""

# Wait for Ctrl+C
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $ELECTRON_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    lsof -ti:8500 | xargs kill -9 2>/dev/null
    echo "Done. Goodbye!"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait $ELECTRON_PID 2>/dev/null
cleanup
