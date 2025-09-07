#!/bin/bash
# GitHub Actions Setup Helper
# Gets Railway project information for GitHub secrets

echo "🔍 GitHub Actions Railway Setup Helper"
echo "======================================"

# Check if Railway CLI is installed and authenticated
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

if ! railway whoami > /dev/null 2>&1; then
    echo "❌ Not logged in to Railway CLI"
    echo "   Please run: railway login"
    exit 1
fi

echo "✅ Railway CLI authenticated as: $(railway whoami)"
echo ""

echo "📋 Available Railway Projects:"
echo "=============================="
railway list
echo ""

echo "🔐 GitHub Secrets Setup Information:"
echo "===================================="

echo ""
echo "1️⃣  RAILWAY_TOKEN:"
echo "   Get your Railway token by running: railway auth"
echo "   Or get from Railway dashboard: Settings → Tokens"
echo ""

echo "2️⃣  RAILWAY_PROJECT_ID (Production):"
echo "   Link to your production project:"
read -p "   Enter production project name: " PROD_PROJECT

if [ ! -z "$PROD_PROJECT" ]; then
    echo "   Linking to production project..."
    if railway link --project "$PROD_PROJECT" > /dev/null 2>&1; then
        PROD_ID=$(railway status | grep "Project:" | awk '{print $2}' | xargs)
        echo "   ✅ Production Project ID: $PROD_ID"
    else
        echo "   ❌ Failed to link to production project"
    fi
fi

echo ""
echo "3️⃣  RAILWAY_STAGING_PROJECT_ID (Optional):"
echo "   Link to your staging/test project:"
read -p "   Enter staging project name (or press Enter to skip): " STAGING_PROJECT

if [ ! -z "$STAGING_PROJECT" ]; then
    echo "   Linking to staging project..."
    if railway link --project "$STAGING_PROJECT" > /dev/null 2>&1; then
        STAGING_ID=$(railway status | grep "Project:" | awk '{print $2}' | xargs)
        echo "   ✅ Staging Project ID: $STAGING_ID"
    else
        echo "   ❌ Failed to link to staging project"
    fi
fi

echo ""
echo "🎯 GitHub Secrets to Add:"
echo "========================"
echo "Go to: Bob8259/new-bytewise-frontend → Settings → Secrets → Actions"
echo ""
echo "Add these secrets:"
echo "RAILWAY_TOKEN = [your-railway-token]"
if [ ! -z "$PROD_ID" ]; then
    echo "RAILWAY_PROJECT_ID = $PROD_ID"
fi
if [ ! -z "$STAGING_ID" ]; then
    echo "RAILWAY_STAGING_PROJECT_ID = $STAGING_ID"
fi

echo ""
echo "✅ Setup complete! Bob can now:"
echo "   1. Add the secrets to GitHub"
echo "   2. Push code to main branch"
echo "   3. Watch automatic deployment! 🚀"
