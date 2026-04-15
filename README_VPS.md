# VPS Deployment Guide - Polymarket Bot

Complete guide to deploy the Polymarket bot on a Linux VPS.

---

## Prerequisites

- **VPS**: Ubuntu 22.04 or 24.04 recommended (1GB RAM minimum)
- **Domain**: Optional, but recommended for security
- **GitHub Access**: To clone the repository

---

## Quick Start (One-Command Setup)

```bash
# SSH into your VPS, then run:
curl -fsSL https://raw.githubusercontent.com/Decka-tan/poly-bot/main/deploy.sh | bash
```

Or manually follow the steps below.

---

## Manual Setup

### Step 1: Update System & Install Dependencies

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ and essentials
sudo apt install -y python3.11 python3.11-venv python3-pip git curl

# Verify Python version
python3 --version  # Should be 3.11+
```

### Step 2: Create Bot Directory

```bash
# Create directory
mkdir -p ~/poly-bot
cd ~/poly-bot

# Clone your repository
git clone https://github.com/Decka-tan/poly-bot.git .

# Or if repo is private, use SSH:
# git clone git@github.com:Decka-tan/poly-bot.git .
```

### Step 3: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Create .env file
nano .env
```

Copy your `.env` content:

```bash
# Polymarket Credentials
POLYMARKET_PRIVATE_KEY=your_private_key_here
POLYMARKET_FUNDER=
POLYMARKET_API_KEY=your_api_key
POLYMARKET_API_SECRET=your_api_secret
POLYMARKET_API_PASSPHRASE=your_passphrase

# Relayer API (Gas-free claims)
RELAYER_API_KEY=
RELAYER_API_KEY_ADDRESS=

# Bot Config
DRY_RUN=false                    # Set to false for live trading
BET_AMOUNT=3.0
LATE_BET_AMOUNT=4.0
MIN_ODDS=0.45
MAX_ODDS=0.95
LIQUIDATION_THRESHOLD=200000

# Auto Claim
AUTO_REDEEM_ENABLED=true
AUTO_CLAIM_INTERVAL_MINUTES=3
CLAIM_CASH_THRESHOLD=4.0
```

**Save**: Ctrl+O, Enter, Ctrl+X

### Step 5: Secure .env File

```bash
# Restrict permissions (owner read/write only)
chmod 600 .env

# Verify
ls -la .env  # Should show -rw-------
```

### Step 6: Create Logs Directory

```bash
mkdir -p logs
```

### Step 7: Test Run (Manual)

```bash
# Activate venv if not already
source ~/poly-bot/venv/bin/

# Run bot manually to test
cd ~/poly-bot
python bot_late.py
```

Press Ctrl+C to stop. Check logs:
```bash
tail -f logs/late_live.log
```

---

## Run as Systemd Service (Auto-Restart)

Systemd will:
- Start bot on VPS boot
- Auto-restart on crash
- Keep bot running after SSH logout

### Install Service

```bash
# Copy service file
sudo cp ~/poly-bot/poly-bot.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable poly-bot.service

# Start service now
sudo systemctl start poly-bot.service
```

### Service Management

```bash
# Check status
sudo systemctl status poly-bot.service

# View logs
sudo journalctl -u poly-bot.service -f

# Restart service
sudo systemctl restart poly-bot.service

# Stop service
sudo systemctl stop poly-bot.service

# Disable auto-start
sudo systemctl disable poly-bot.service
```

---

## Run with tmux (Alternative)

If you prefer tmux over systemd:

```bash
# Install tmux
sudo apt install -y tmux

# Create new session
tmux new -s polybot

# Activate venv and run bot
cd ~/poly-bot
source venv/bin/activate
python bot_late.py

# Detach from session: Ctrl+B, then D
# Reattach later: tmux attach -t polybot
```

---

## Monitoring

### Check Bot Logs

```bash
# Main bot log
tail -f ~/poly-bot/logs/late_live.log

# Bet history
tail -f ~/poly-bot/logs/bets.csv

# Blocked signals
tail -f ~/poly-bot/logs/late_live_blocked.csv
```

### Check System Resources

```bash
# CPU & Memory
htop

# Disk space
df -h

# Network activity
iftop
```

### Set Up Log Rotation (Optional)

Prevent logs from growing too large:

```bash
sudo nano /etc/logrotate.d/poly-bot
```

```
/home/youruser/poly-bot/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 youruser youruser
}
```

---

## Updates

### Update Bot from GitHub

```bash
cd ~/poly-bot
git pull origin main

# Restart service
sudo systemctl restart poly-bot.service
```

Or use the update script:
```bash
~/poly-bot/update.sh
```

---

## Firewall Configuration

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## Troubleshooting

### Bot won't start

```bash
# Check service status for errors
sudo systemctl status poly-bot.service

# View detailed logs
sudo journalctl -u poly-bot.service -n 50
```

### Python module not found

```bash
# Activate venv and reinstall
cd ~/poly-bot
source venv/bin/activate
pip install -r requirements.txt
```

### .env file permissions

```bash
# Fix permissions
chmod 600 ~/poly-bot/.env
chown $USER:$USER ~/poly-bot/.env
```

### WebSocket connection issues

```bash
# Check internet connectivity
ping api.hyperliquid.xyz
ping clob.polymarket.com

# Check DNS
nslookup api.hyperliquid.xyz
```

---

## Security Best Practices

1. **Never commit .env to git** (already in .gitignore)
2. **Use SSH keys** for GitHub access
3. **Set strong SSH password** or use key-based auth
4. **Keep system updated**: `sudo apt update && sudo apt upgrade -y`
5. **Use separate wallet** for bot (not your main wallet)
6. **Start with small bet amounts** and DRY_RUN=true

---

## VPS Recommendations

| Provider | Minimum Specs | Est. Cost/Month |
|----------|---------------|-----------------|
| DigitalOcean | 1GB RAM, 1 CPU | $6 |
| Linode | 1GB RAM, 1 CPU | $5 |
| Vultr | 1GB RAM, 1 CPU | $5 |
| Hetzner | 2GB RAM, 1 CPU | €4 |

---

## File Structure After Setup

```
~/poly-bot/
├── venv/                  # Virtual environment
├── logs/                  # Log files
│   ├── late_live.log
│   ├── bets.csv
│   └── late_live_blocked.csv
├── .env                   # Configuration (chmod 600)
├── bot_late.py           # Main bot
├── claim_bot.py          # Auto-claim bot
├── poly-bot.service      # Systemd service file
├── deploy.sh             # Deployment script
└── update.sh             # Update script
```
