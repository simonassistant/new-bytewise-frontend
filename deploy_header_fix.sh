#!/bin/bash

echo "🎨 Deploying header repositioning: Move LANG 0036 header to top level..."

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf dist_header_fix.tar.gz dist/

# Upload to server
echo "⬆️ Uploading to server..."
echo "Password: 'Tew52025!st6@t23GH4B@F%5&k82yU'"
scp dist_header_fix.tar.gz root@8.211.158.223:/tmp/

# Deploy on server
echo "🚀 Deploying header fix..."
ssh root@8.211.158.223 << 'ENDSSH'

echo "📄 Extracting updated files..."
cd /var/www/aiedit.hkbu.tech
tar -xzf /tmp/dist_header_fix.tar.gz --strip-components=1

echo "🔧 Setting permissions..."
chown -R www-data:www-data /var/www/aiedit.hkbu.tech 2>/dev/null || chown -R nginx:nginx /var/www/aiedit.hkbu.tech
chmod -R 755 /var/www/aiedit.hkbu.tech

echo "✅ Header repositioning deployed!"

# Cleanup
rm -f /tmp/dist_header_fix.tar.gz

ENDSSH

# Local cleanup
rm -f dist_header_fix.tar.gz

echo ""
echo "🎉 Header repositioning deployment complete!"
echo "📍 Test the updated header at: http://aiedit.hkbu.tech/writingbot"
echo ""
echo "✨ What changed:"
echo "   📍 LANG 0036 header now appears at the TOP of all modes"
echo "   🎯 Consistent branding across Briefing, Training, and Assessment modes"
echo "   🧹 Removed duplicate header from Briefing mode"
echo ""
echo "🔍 Expected result: Beautiful gradient header visible in all three modes!"
