#!/bin/bash

echo "🔄 Quick update: Deploy iframe fix to server..."

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf dist_iframe_fix.tar.gz dist/

# Upload to server
echo "⬆️ Uploading to server..."
echo "Password: 'Tew52025!st6@t23GH4B@F%5&k82yU'"
scp dist_iframe_fix.tar.gz root@8.211.158.223:/tmp/

# Deploy on server
echo "🚀 Deploying iframe fix..."
ssh root@8.211.158.223 << 'ENDSSH'

echo "📁 Backing up current deployment..."
cp -r /var/www/aiedit.hkbu.tech /var/www/aiedit.hkbu.tech.backup.$(date +%H%M%S)

echo "📄 Extracting new files..."
cd /var/www/aiedit.hkbu.tech
tar -xzf /tmp/dist_iframe_fix.tar.gz --strip-components=1

echo "🔧 Setting permissions..."
chown -R www-data:www-data /var/www/aiedit.hkbu.tech 2>/dev/null || chown -R nginx:nginx /var/www/aiedit.hkbu.tech
chmod -R 755 /var/www/aiedit.hkbu.tech

echo "🧪 Testing key files..."
ls -la /var/www/aiedit.hkbu.tech/briefing.html

echo "✅ Iframe fix deployed!"

# Cleanup
rm -f /tmp/dist_iframe_fix.tar.gz

ENDSSH

# Local cleanup
rm -f dist_iframe_fix.tar.gz

echo ""
echo "🎉 Iframe fix deployment complete!"
echo "📍 Test your iframe at: http://aiedit.hkbu.tech/writingbot"
echo "📄 Test briefing.html directly: http://aiedit.hkbu.tech/briefing.html"
