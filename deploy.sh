#!/bin/bash
# Railway CLI Deployment Script for ByteWise Frontend
# Usage: ./deploy.sh [project-name] [environment]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
PROJECT_NAME=${1:-"Avatartutor.hkbu.tech"}
ENVIRONMENT=${2:-"production"}

echo -e "${BLUE}🚀 Railway CLI Deployment Script${NC}"
echo -e "${BLUE}=================================${NC}"

# Check Railway CLI authentication
echo -e "${YELLOW}🔍 Checking Railway CLI status...${NC}"
if ! railway whoami > /dev/null 2>&1; then
    echo -e "${RED}❌ Not logged in to Railway CLI${NC}"
    echo -e "${YELLOW}Please run: railway login${NC}"
    exit 1
fi

RAILWAY_USER=$(railway whoami)
echo -e "${GREEN}✅ Logged in as: ${RAILWAY_USER}${NC}"

# Link to project
echo -e "${YELLOW}🔗 Linking to project: ${PROJECT_NAME}...${NC}"
if ! railway link --project "${PROJECT_NAME}"; then
    echo -e "${RED}❌ Failed to link to project: ${PROJECT_NAME}${NC}"
    echo -e "${YELLOW}Available projects:${NC}"
    railway list
    exit 1
fi

# Show current project info
echo -e "${YELLOW}📋 Current project configuration:${NC}"
railway status

# Set environment variables based on environment
echo -e "${YELLOW}⚙️  Setting environment variables for ${ENVIRONMENT}...${NC}"

case $ENVIRONMENT in
    "production")
        railway variables --set "NODE_ENV=production" --set "VITE_APP_DOMAIN=https://avatartutor.hkbu.tech" --set "VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api" --set "VITE_APP_TITLE=ByteWise Avatar Tutor"
        ;;
    "staging")
        railway variables --set "NODE_ENV=staging" --set "VITE_APP_DOMAIN=https://avatar-test.hkbu.tech" --set "VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api" --set "VITE_APP_TITLE=ByteWise Avatar Tutor (Test)"
        ;;
    *)
        echo -e "${YELLOW}⚠️  Unknown environment: ${ENVIRONMENT}, using production defaults${NC}"
        railway variables --set "NODE_ENV=production"
        ;;
esac

echo -e "${GREEN}✅ Environment variables set${NC}"

# Show current variables
echo -e "${YELLOW}📊 Current environment variables:${NC}"
railway variables

# Deploy
echo -e "${YELLOW}📦 Building and deploying...${NC}"
echo -e "${BLUE}This may take a few minutes...${NC}"

if railway up --detach; then
    echo -e "${GREEN}✅ Deployment initiated successfully!${NC}"
    
    # Show deployment info
    echo -e "${YELLOW}🌐 Domain information:${NC}"
    railway domain
    
    # Show recent logs
    echo -e "${YELLOW}📝 Recent deployment logs:${NC}"
    sleep 5  # Wait a moment for deployment to start
    railway logs -b
    
    echo -e "${GREEN}🎉 Deployment completed!${NC}"
    echo -e "${BLUE}Monitor logs with: railway logs -b${NC}"
    echo -e "${BLUE}Check status with: railway status${NC}"
    
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo -e "${YELLOW}📝 Error logs:${NC}"
    railway logs -b
    exit 1
fi
