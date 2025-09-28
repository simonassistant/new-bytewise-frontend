#!/bin/bash

echo "🔧 Configuring nginx for IP access (8.211.158.223)..."

# Connect to server and update nginx configuration for IP access
ssh root@8.211.158.223 << 'ENDSSH'

echo "📋 Setting up nginx for IP access..."

# Create a configuration that handles both IP and future domain access
cat > /etc/nginx/conf.d/writingbot.conf << 'EOF'
server {
    listen 80 default_server;
    server_name 8.211.158.223 aiedit.hkbu.tech www.aiedit.hkbu.tech _;
    root /var/www/aiedit.hkbu.tech;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Handle Vue.js routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Poe API proxy
    location /poe_api/ {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # General API proxy
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# Remove conflicting configurations
echo "🗑️ Removing conflicting nginx configurations..."
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/conf.d/default.conf
rm -f /etc/nginx/conf.d/aiedit.hkbu.tech.conf

# Check if files exist in web directory
echo "📁 Checking web directory contents..."
ls -la /var/www/aiedit.hkbu.tech/

# Verify index.html exists
if [ -f "/var/www/aiedit.hkbu.tech/index.html" ]; then
    echo "✅ index.html found"
    echo "📄 index.html preview:"
    head -5 /var/www/aiedit.hkbu.tech/index.html
else
    echo "❌ index.html not found!"
    echo "📂 Directory contents:"
    ls -la /var/www/aiedit.hkbu.tech/
fi

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"

    # Reload nginx
    echo "🔄 Reloading nginx..."
    systemctl reload nginx

    echo "✅ Nginx reloaded successfully"
    echo ""
    echo "🎉 Configuration complete!"
    echo "📍 Your WritingBot should now be accessible at:"
    echo "   http://8.211.158.223"
    echo ""
    echo "🔍 Testing local access..."
    curl -s -I http://localhost | head -3

else
    echo "❌ Nginx configuration has errors"
    nginx -t
    exit 1
fi

echo ""
echo "📋 Active nginx configurations:"
ls -la /etc/nginx/conf.d/

ENDSSH

echo ""
echo "✅ IP access configuration complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Test: http://8.211.158.223 (should show your WritingBot)"
echo "2. Later: Set up DNS for aiedit.hkbu.tech (when ready)"
echo "3. Optional: Add SSL certificate"
echo ""
echo "💡 The current configuration will work for both:"
echo "   - IP access: http://8.211.158.223"
echo "   - Domain access: http://aiedit.hkbu.tech (once DNS is set up)"
