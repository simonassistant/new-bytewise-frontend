#!/bin/bash

echo "🎨 Deploying UI simplification: Remove skills section and progress tracking..."

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf dist_ui_simplified.tar.gz dist/

# Upload to server
echo "⬆️ Uploading to server..."
echo "Password: 'Tew52025!st6@t23GH4B@F%5&k82yU'"
scp dist_ui_simplified.tar.gz root@8.211.158.223:/tmp/

# Deploy on server
echo "🚀 Deploying UI simplification..."
ssh root@8.211.158.223 << 'ENDSSH'

echo "📄 Extracting updated files..."
cd /var/www/aiedit.hkbu.tech
tar -xzf /tmp/dist_ui_simplified.tar.gz --strip-components=1

echo "🔧 Setting permissions..."
chown -R www-data:www-data /var/www/aiedit.hkbu.tech 2>/dev/null || chown -R nginx:nginx /var/www/aiedit.hkbu.tech
chmod -R 755 /var/www/aiedit.hkbu.tech

echo "✅ UI simplification deployed!"

# Cleanup
rm -f /tmp/dist_ui_simplified.tar.gz

ENDSSH

# Local cleanup
rm -f dist_ui_simplified.tar.gz

echo ""
echo "🎉 UI simplification deployment complete!"
echo "📍 Test your simplified interface at: http://aiedit.hkbu.tech/writingbot"
echo ""
echo "✨ What was removed:"
echo "   ❌ 'Hide Skills' / 'Show Skills' button"
echo "   ❌ 'Skills Being Developed' section"
echo "   ❌ 'Session Progress' tracking display"
echo ""
echo "🎯 Result: Cleaner, more focused interface for training and assessment modes"
