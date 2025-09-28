#!/bin/bash

echo "🎨 Deploying branding update: EditForge → LANG 0036..."

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf dist_branding_update.tar.gz dist/

# Upload to server
echo "⬆️ Uploading to server..."
echo "Password: 'Tew52025!st6@t23GH4B@F%5&k82yU'"
scp dist_branding_update.tar.gz root@8.211.158.223:/tmp/

# Deploy on server
echo "🚀 Deploying branding update..."
ssh root@8.211.158.223 << 'ENDSSH'

echo "📄 Extracting updated files..."
cd /var/www/aiedit.hkbu.tech
tar -xzf /tmp/dist_branding_update.tar.gz --strip-components=1

echo "🔧 Setting permissions..."
chown -R www-data:www-data /var/www/aiedit.hkbu.tech 2>/dev/null || chown -R nginx:nginx /var/www/aiedit.hkbu.tech
chmod -R 755 /var/www/aiedit.hkbu.tech

echo "✅ Branding update deployed!"

# Cleanup
rm -f /tmp/dist_branding_update.tar.gz

ENDSSH

# Local cleanup
rm -f dist_branding_update.tar.gz

echo ""
echo "🎉 Branding update deployment complete!"
echo "📍 Check updated branding at: http://aiedit.hkbu.tech/writingbot"
echo ""
echo "✨ Updated branding:"
echo "   Old: EditForge: Human-AI Collaboration System"
echo "   New: LANG 0036: AI Writing Collaboration Lab"
echo ""
echo "   Old: Practice and assess your AI interaction skills"
echo "   New: Develop and demonstrate AI literacy and human-AI partnership"
