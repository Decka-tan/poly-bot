#!/bin/bash
# update.sh - Update bot from GitHub and restart service

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BOT_DIR="$HOME/poly-bot"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Polymarket Bot - Update Script                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

cd "$BOT_DIR"

# Save current commit
OLD_COMMIT=$(git rev-parse --short HEAD)

# Stop service
echo -e "${YELLOW}→ Stopping bot service...${NC}"
sudo systemctl stop poly-bot.service

# Pull latest changes
echo -e "${YELLOW}→ Pulling latest changes from GitHub...${NC}"
git pull origin main

# Update dependencies if requirements.txt changed
if git diff --name-only $OLD_COMMIT HEAD | grep -q "requirements.txt"; then
    echo -e "${YELLOW}→ requirements.txt changed, updating dependencies...${NC}"
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Start service
echo -e "${YELLOW}→ Starting bot service...${NC}"
sudo systemctl start poly-bot.service

# Show status
echo ""
echo -e "${GREEN}✓ Update complete!${NC}"
echo ""
echo -e "Service status:"
sudo systemctl status poly-bot.service --no-pager -l
echo ""
echo -e "${BLUE}View logs: tail -f $BOT_DIR/logs/late_live.log${NC}"
