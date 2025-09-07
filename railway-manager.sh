#!/bin/bash
# Railway Project Management Script
# Quickly switch between and manage Railway projects

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_help() {
    echo -e "${BLUE}Railway Project Manager${NC}"
    echo ""
    echo "Usage: ./railway-manager.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  list                    - List all projects"
    echo "  link <project-name>     - Link to a specific project"
    echo "  status                  - Show current project status"
    echo "  vars                    - List environment variables"
    echo "  logs [lines]            - Show logs (default: 50 lines)"
    echo "  domain                  - Show domain configuration"
    echo "  deploy                  - Quick deploy current branch"
    echo "  restart                 - Restart the service"
    echo ""
    echo "Examples:"
    echo "  ./railway-manager.sh list"
    echo "  ./railway-manager.sh link \"Avatartutor.hkbu.tech\""
    echo "  ./railway-manager.sh deploy"
    echo "  ./railway-manager.sh logs 100"
}

case "$1" in
    "list")
        echo -e "${YELLOW}📋 Available Railway Projects:${NC}"
        railway list
        ;;
    "link")
        if [ -z "$2" ]; then
            echo -e "${YELLOW}📋 Available projects:${NC}"
            railway list
            echo ""
            echo -e "${YELLOW}Usage: ./railway-manager.sh link \"Project Name\"${NC}"
            exit 1
        fi
        echo -e "${YELLOW}🔗 Linking to project: $2${NC}"
        railway link --project "$2"
        ;;
    "status")
        echo -e "${YELLOW}📊 Current project status:${NC}"
        railway status
        ;;
    "vars")
        echo -e "${YELLOW}⚙️  Environment variables:${NC}"
        railway variables
        ;;
    "logs")
        echo -e "${YELLOW}📝 Build logs:${NC}"
        railway logs -b
        ;;
    "domain")
        echo -e "${YELLOW}🌐 Domain configuration:${NC}"
        railway domain
        ;;
    "deploy")
        echo -e "${YELLOW}🚀 Deploying current branch...${NC}"
        railway up
        ;;
    "restart")
        echo -e "${YELLOW}🔄 Restarting service...${NC}"
        railway restart
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        echo -e "${YELLOW}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
