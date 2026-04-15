#!/bin/bash
# deploy.sh - Automated VPS deployment script for Polymarket Bot
# Usage: curl -fsSL https://raw.githubusercontent.com/Decka-tan/poly-bot/main/deploy.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BOT_DIR="$HOME/poly-bot"
SERVICE_FILE="/etc/systemd/system/poly-bot.service"
REPO_URL="https://github.com/Decka-tan/poly-bot.git"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        Polymarket Bot - VPS Deployment Script             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}✗ Don't run this script as root! Run as regular user.${NC}"
    exit 1
fi

# Step 1: Update system
echo -e "${YELLOW}[1/7] Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Step 2: Install dependencies
echo -e "${YELLOW}[2/7] Installing Python 3.11+ and dependencies...${NC}"
sudo apt install -y python3.11 python3.11-venv python3-pip git curl tmux

# Verify Python version
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Step 3: Create bot directory
echo -e "${YELLOW}[3/7] Setting up bot directory...${NC}"
if [ -d "$BOT_DIR" ]; then
    echo -e "${YELLOW}⚠ Directory exists, pulling latest changes...${NC}"
    cd "$BOT_DIR"
    git pull origin main
else
    echo -e "${BLUE}→ Cloning repository...${NC}"
    git clone "$REPO_URL" "$BOT_DIR"
    cd "$BOT_DIR"
fi

# Step 4: Create virtual environment
echo -e "${YELLOW}[4/7] Creating Python virtual environment...${NC}"
if [ ! -d "$BOT_DIR/venv" ]; then
    python3 -m venv "$BOT_DIR/venv"
fi
source "$BOT_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$BOT_DIR/requirements.txt"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 5: Create .env file
echo -e "${YELLOW}[5/7] Setting up configuration...${NC}"
if [ ! -f "$BOT_DIR/.env" ]; then
    echo -e "${BLUE}→ Creating .env file...${NC}"
    cp "$BOT_DIR/.env.example" "$BOT_DIR/.env" 2>/dev/null || cat > "$BOT_DIR/.env" << 'EOF'
# Polymarket Credentials (FILL THESE IN!)
POLYMARKET_PRIVATE_KEY=
POLYMARKET_FUNDER=
POLYMARKET_API_KEY=
POLYMARKET_API_SECRET=
POLYMARKET_API_PASSPHRASE=

# Relayer API
RELAYER_API_KEY=
RELAYER_API_KEY_ADDRESS=

# Bot Config
DRY_RUN=true
BET_AMOUNT=3.0
LATE_BET_AMOUNT=4.0
MIN_ODDS=0.45
MAX_ODDS=0.95
LIQUIDATION_THRESHOLD=200000

# Auto Claim
AUTO_REDEEM_ENABLED=true
AUTO_CLAIM_INTERVAL_MINUTES=3
CLAIM_CASH_THRESHOLD=4.0
EOF
    chmod 600 "$BOT_DIR/.env"
    echo -e "${RED}✗ EDIT .env FILE WITH YOUR CREDENTIALS BEFORE RUNNING!${NC}"
    echo -e "${YELLOW}  Run: nano ~/poly-bot/.env${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Secure .env
chmod 600 "$BOT_DIR/.env"

# Step 6: Create logs directory
echo -e "${YELLOW}[6/7] Setting up logs directory...${NC}"
mkdir -p "$BOT_DIR/logs"
echo -e "${GREEN}✓ Logs directory created${NC}"

# Step 7: Setup systemd service
echo -e "${YELLOW}[7/7] Setting up systemd service...${NC}"
# Get current username
USERNAME=$(whoami)
USERHOME=$(eval echo ~$USERNAME)

# Create service file with correct paths
sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Polymarket Late Entry Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USERNAME
Group=$USERNAME
WorkingDirectory=$BOT_DIR

# Activate virtual environment and run bot
Environment=PATH=$BOT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$BOT_DIR/venv/bin/python bot_late.py

# Auto-restart configuration
Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3

# Logging
StandardOutput=append:$BOT_DIR/logs/service.log
StandardError=append:$BOT_DIR/logs/service_error.log

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload
sudo systemctl enable poly-bot.service
echo -e "${GREEN}✓ Systemd service configured${NC}"

# Done!
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  Deployment Complete! ✓                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${YELLOW}IMPORTANT: Complete these steps before running:${NC}"
echo ""
echo -e "  1. ${RED}Edit .env with your credentials:${NC}"
echo -e "     ${BLUE}nano ~/poly-bot/.env${NC}"
echo ""
echo -e "  2. ${RED}Generate API credentials (if needed):${NC}"
echo -e "     ${BLUE}cd ~/poly-bot && source venv/bin/activate${NC}"
echo -e "     ${BLUE}python generate_api_creds.py${NC}"
echo ""
echo -e "  3. ${GREEN}Start the bot:${NC}"
echo -e "     ${BLUE}sudo systemctl start poly-bot.service${NC}"
echo ""
echo -e "  4. ${GREEN}Check status:${NC}"
echo -e "     ${BLUE}sudo systemctl status poly-bot.service${NC}"
echo ""
echo -e "  5. ${GREEN}View logs:${NC}"
echo -e "     ${BLUE}tail -f ~/poly-bot/logs/late_live.log${NC}"
echo ""
echo -e "${YELLOW}Service Management Commands:${NC}"
echo -e "  Start:   ${BLUE}sudo systemctl start poly-bot.service${NC}"
echo -e "  Stop:    ${BLUE}sudo systemctl stop poly-bot.service${NC}"
echo -e "  Restart: ${BLUE}sudo systemctl restart poly-bot.service${NC}"
echo -e "  Status:  ${BLUE}sudo systemctl status poly-bot.service${NC}"
echo -e "  Logs:    ${BLUE}sudo journalctl -u poly-bot.service -f${NC}"
echo ""
