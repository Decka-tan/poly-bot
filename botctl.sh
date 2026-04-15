#!/bin/bash
# botctl.sh - Simple bot control script
# Usage: ./botctl.sh [start|stop|restart|status|logs]

ACTION=${1:-status}
BOT_DIR="$HOME/poly-bot"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

case "$ACTION" in
    start)
        echo -e "${BLUE}Starting Polymarket Bot...${NC}"
        sudo systemctl start poly-bot.service
        echo -e "${GREEN}✓ Bot started${NC}"
        echo -e "${BLUE}Check status: ./botctl.sh status${NC}"
        ;;

    stop)
        echo -e "${YELLOW}Stopping Polymarket Bot...${NC}"
        sudo systemctl stop poly-bot.service
        echo -e "${GREEN}✓ Bot stopped${NC}"
        ;;

    restart)
        echo -e "${YELLOW}Restarting Polymarket Bot...${NC}"
        sudo systemctl restart poly-bot.service
        echo -e "${GREEN}✓ Bot restarted${NC}"
        ./botctl.sh status
        ;;

    status)
        sudo systemctl status poly-bot.service --no-pager
        ;;

    logs)
        echo -e "${BLUE}Showing bot logs (Ctrl+C to exit):${NC}"
        tail -f "$BOT_DIR/logs/late_live.log"
        ;;

    service-logs)
        echo -e "${BLUE}Showing service logs (Ctrl+C to exit):${NC}"
        sudo journalctl -u poly-bot.service -f
        ;;

    update)
        "$BOT_DIR/update.sh"
        ;;

    *)
        echo "Usage: ./botctl.sh [start|stop|restart|status|logs|service-logs|update]"
        echo ""
        echo "Commands:"
        echo "  start         - Start the bot service"
        echo "  stop          - Stop the bot service"
        echo "  restart       - Restart the bot service"
        echo "  status        - Show service status"
        echo "  logs          - Show bot log file"
        echo "  service-logs  - Show systemd journal logs"
        echo "  update        - Update bot from GitHub"
        exit 1
        ;;
esac
