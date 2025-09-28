#!/bin/bash

# Deploy to HKBU Server Script
echo "=== Deploying WritingBot to HKBU Server ==="

# Build the project
echo "Building the project..."
npm run build

# Create backup of current deployment (optional)
echo "Creating backup..."
ssh YOUR_HKBU_USERNAME@YOUR_HKBU_SERVER "cp -r /path/to/current/writingBot /path/to/backup/writingBot_$(date +%Y%m%d_%H%M%S)"

# Upload new version
echo "Uploading new version..."
rsync -avz --delete dist/ YOUR_HKBU_USERNAME@YOUR_HKBU_SERVER:/path/to/writingBot/

echo "=== Deployment Complete ==="
echo "Please update the placeholders in this script:"
echo "- YOUR_HKBU_USERNAME: Your HKBU username"
echo "- YOUR_HKBU_SERVER: HKBU server address"
echo "- /path/to/writingBot/: Actual path on HKBU server"
