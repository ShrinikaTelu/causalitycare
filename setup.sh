#!/bin/bash
# CausalityCare Quick Start & Management Commands

echo "🚀 CausalityCare Frontend Fix - Quick Reference"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_status() {
    echo -e "\n${BLUE}📊 System Status${NC}"
    echo "─────────────────────────────────"
    
    # Check backend
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend${NC}:   http://localhost:8000 (Running)"
        BACKEND_STATUS=$(curl -s http://localhost:8000/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        echo "   Status: $BACKEND_STATUS"
    else
        echo -e "${RED}❌ Backend${NC}:   http://localhost:8000 (Not Running)"
    fi
    
    # Check frontend
    if curl -s http://localhost:4200/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend${NC}:  http://localhost:4200 (Running)"
    else
        echo -e "${RED}❌ Frontend${NC}:  http://localhost:4200 (Not Running)"
    fi
}

start_all() {
    echo -e "\n${BLUE}🚀 Starting Services${NC}"
    echo "─────────────────────────────────"
    
    # Start backend
    echo "Starting backend..."
    cd /Users/shrinikatelu/causalitycare/backend
    python3 main.py > /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID)"
    
    # Wait a moment
    sleep 3
    
    # Start frontend
    echo "Starting frontend..."
    cd /Users/shrinikatelu/causalitycare/frontend
    npm start > /tmp/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓${NC} Frontend started (PID: $FRONTEND_PID)"
    
    sleep 5
    
    # Show status
    show_status
    
    echo -e "\n${GREEN}✅ All services started!${NC}"
    echo "Open your browser: http://localhost:4200"
}

stop_all() {
    echo -e "\n${BLUE}🛑 Stopping Services${NC}"
    echo "─────────────────────────────────"
    
    # Kill backend
    echo "Stopping backend..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓${NC} Backend stopped"
    
    # Kill frontend
    echo "Stopping frontend..."
    lsof -ti:4200 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓${NC} Frontend stopped"
    
    echo -e "\n${GREEN}✅ All services stopped!${NC}"
}

restart_all() {
    echo -e "${YELLOW}🔄 Restarting all services...${NC}"
    stop_all
    sleep 2
    start_all
}

test_api() {
    echo -e "\n${BLUE}🧪 Testing API${NC}"
    echo "─────────────────────────────────"
    
    # Test health endpoint
    echo "Testing /health endpoint..."
    HEALTH=$(curl -s http://localhost:8000/health)
    if echo "$HEALTH" | grep -q "healthy"; then
        echo -e "${GREEN}✓${NC} Backend is healthy"
        echo "Response: $HEALTH"
    else
        echo -e "${RED}✗${NC} Backend is not responding"
    fi
    
    # Test analyze endpoint
    echo -e "\nTesting /analyze endpoint..."
    RESPONSE=$(curl -s -X POST http://localhost:8000/analyze \
        -F "text=Test analysis" \
        -F "image=@/Users/shrinikatelu/causalitycare/backend/test_image.jpg" 2>/dev/null)
    
    if echo "$RESPONSE" | grep -q "mood_board"; then
        echo -e "${GREEN}✓${NC} API returns mood_board"
        echo "Sample response:"
        echo "$RESPONSE" | jq '.mood_board.interpretation_confidence' 2>/dev/null || echo "$RESPONSE" | head -c 200
    else
        echo -e "${YELLOW}⚠${NC} No mood_board in response"
    fi
}

open_app() {
    echo -e "\n${BLUE}🌐 Opening Application${NC}"
    echo "─────────────────────────────────"
    
    if command -v open &> /dev/null; then
        open http://localhost:4200
        echo -e "${GREEN}✓${NC} Opening http://localhost:4200 in browser"
    else
        echo "Open http://localhost:4200 in your browser"
    fi
}

view_logs() {
    echo -e "\n${BLUE}📋 Viewing Logs${NC}"
    echo "─────────────────────────────────"
    
    if [ -f /tmp/backend.log ]; then
        echo "Backend logs:"
        tail -20 /tmp/backend.log
    fi
    
    if [ -f /tmp/frontend.log ]; then
        echo -e "\nFrontend logs:"
        tail -20 /tmp/frontend.log
    fi
}

clear_cache() {
    echo -e "\n${BLUE}🧹 Clearing Cache${NC}"
    echo "─────────────────────────────────"
    
    echo "Clearing frontend node_modules..."
    rm -rf /Users/shrinikatelu/causalitycare/frontend/node_modules
    echo -e "${GREEN}✓${NC} Cleared node_modules"
    
    echo "Reinstalling dependencies..."
    cd /Users/shrinikatelu/causalitycare/frontend
    npm install > /tmp/npm_install.log 2>&1
    echo -e "${GREEN}✓${NC} Dependencies reinstalled"
}

show_help() {
    cat << 'EOF'

CausalityCare Frontend Fix - Command Reference
═══════════════════════════════════════════════

Usage: source setup.sh && <command>

COMMANDS:
  status          - Show current system status
  start           - Start all services
  stop            - Stop all services
  restart         - Restart all services
  test            - Test API endpoints
  open            - Open application in browser
  logs            - View service logs
  clean           - Clear cache and reinstall dependencies
  help            - Show this help message

EXAMPLES:
  status          # Check if services are running
  start           # Start backend and frontend
  test            # Verify API is working
  open            # Launch app in browser
  restart         # Restart all services
  logs            # View application logs

QUICK START:
  1. Start services:    start
  2. Check status:      status
  3. Open browser:      open
  4. Test API:          test

PORTS:
  Frontend:  http://localhost:4200
  Backend:   http://localhost:8000 (API)
  API Health: http://localhost:8000/health

TROUBLESHOOTING:
  Port in use?    → restart
  Build error?    → clean
  API not found?  → test
  Nothing works?  → stop, then start

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For detailed documentation, see:
  • /Users/shrinikatelu/causalitycare/FINAL_SUMMARY.md
  • /Users/shrinikatelu/causalitycare/frontend/TESTING_GUIDE.md
  • /Users/shrinikatelu/causalitycare/backend/FRONTEND_FIX_COMPLETE.md
EOF
}

# Main menu
if [ $# -eq 0 ]; then
    show_help
else
    case "$1" in
        status)     show_status ;;
        start)      start_all ;;
        stop)       stop_all ;;
        restart)    restart_all ;;
        test)       test_api ;;
        open)       open_app ;;
        logs)       view_logs ;;
        clean)      clear_cache ;;
        help|--help|-h)  show_help ;;
        *)          echo "Unknown command: $1"; echo "Run 'setup.sh help' for usage"; exit 1 ;;
    esac
fi
