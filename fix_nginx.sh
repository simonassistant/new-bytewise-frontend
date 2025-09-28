#!/bin/bash

echo "🔧 Fixing nginx configuration for aiedit.hkbu.tech..."

# Connect to server and fix nginx configuration
ssh root@8.211.158.223 << 'ENDSSH'

echo "📋 Checking current nginx configuration..."

# Check if our site config exists
if [ -f "/etc/nginx/conf.d/aiedit.hkbu.tech.conf" ]; then
    echo "✅ Site config exists"
else
    echo "❌ Site config missing - creating it..."

    cat > /etc/nginx/conf.d/aiedit.hkbu.tech.conf << 'EOF'
server {
    listen 80 default_server;
    server_name aiedit.hkbu.tech www.aiedit.hkbu.tech 8.211.158.223 _;
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
fi

# Remove or disable default nginx site
echo "🗑️ Disabling default nginx site..."
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    rm -f /etc/nginx/sites-enabled/default
    echo "✅ Removed default site from sites-enabled"
fi

if [ -f "/etc/nginx/conf.d/default.conf" ]; then
    mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled
    echo "✅ Disabled default.conf"
fi

# Check if files exist in our web directory
echo "📁 Checking web directory..."
ls -la /var/www/aiedit.hkbu.tech/

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"

    # Reload nginx
    echo "🔄 Reloading nginx..."
    systemctl reload nginx

    echo "✅ Nginx reloaded successfully"
    echo "🎉 Your site should now be accessible!"
else
    echo "❌ Nginx configuration has errors"
    exit 1
fi

# Show active nginx sites
echo "📋 Active nginx configurations:"
ls -la /etc/nginx/conf.d/

echo "🔍 Current nginx process status:"
systemctl status nginx --no-pager -l

ENDSSH

echo ""
echo "🎯 Fix complete! Try accessing:"
echo "   http://8.211.158.223"
echo "   http://aiedit.hkbu.tech (if DNS is set up)"
echo ""
echo "If you still see the default page:"
echo "1. Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)"
echo "2. Try in an incognito/private window"
echo "3. Wait a few minutes for changes to propagate"
