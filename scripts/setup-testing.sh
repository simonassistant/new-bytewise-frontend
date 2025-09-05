#!/bin/bash

# ByteWise Frontend Testing Environment Setup
# Run this script to quickly set up your testing environment

set -e

echo "🚀 ByteWise Frontend Testing Environment Setup"
echo "================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "⚠️  Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "🔧 Setting up testing environment..."

# Create testing environment file if it doesn't exist
if [ ! -f ".env.testing" ]; then
    echo "📝 Creating .env.testing file..."
    cat > .env.testing << EOF
NODE_ENV=staging
VITE_APP_TITLE=ByteWise Avatar Tutor (Testing)
VITE_APP_DOMAIN=https://avatar-test.hkbu.tech
VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api
VITE_TESTING_MODE=true
VITE_ENABLE_DEBUG=true
EOF
    echo "✅ Created .env.testing"
else
    echo "ℹ️  .env.testing already exists"
fi

# Test build with testing environment
echo "🏗️  Testing build process..."
VITE_NODE_ENV=staging npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful"
else
    echo "❌ Build failed - please check your code"
    exit 1
fi

echo ""
echo "🎯 Next Steps:"
echo "==============="
echo ""
echo "1. 📋 Railway Project Setup:"
echo "   • Go to https://railway.app/dashboard"
echo "   • Create new project: 'bytewise-frontend-testing'"
echo "   • Connect to: tesolchina/new-bytewise-frontend"
echo ""
echo "2. 🔧 Environment Variables (copy to Railway):"
echo "   NODE_ENV=staging"
echo "   VITE_APP_TITLE=ByteWise Avatar Tutor (Testing)"
echo "   VITE_APP_DOMAIN=https://avatar-test.hkbu.tech"
echo "   VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api"
echo "   VITE_TESTING_MODE=true"
echo "   VITE_ENABLE_DEBUG=true"
echo ""
echo "3. 🌐 Custom Domain:"
echo "   • Add domain: avatar-test.hkbu.tech"
echo "   • Copy CNAME target from Railway"
echo "   • Update DNS at Alibaba Cloud"
echo ""
echo "4. 🧪 Testing:"
echo "   • Push your changes to trigger deployment"
echo "   • Test at https://avatar-test.hkbu.tech/"
echo ""
echo "📚 Full documentation: docs/deployment/RAILWAY_TESTING_SETUP.md"
echo ""
echo "🎉 Testing environment setup complete!"
