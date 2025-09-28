#!/bin/bash

# Deploy WritingBot to Aliyun Server with aiedit.hkbu.tech domain
echo "=== Deploying WritingBot to aiedit.hkbu.tech ==="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found. Please run this script from the project root."
    exit 1
fi

# Run tests before deployment (as per project specification)
echo "Running API endpoint tests..."
if [ -f "test_assessbot.js" ]; then
    node test_assessbot.js
    if [ $? -ne 0 ]; then
        echo "Warning: Some tests failed. Continue? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo "Deployment cancelled."
            exit 1
        fi
    fi
fi

# Build the project
echo "Building the project..."
npm run build

if [ ! -d "dist" ]; then
    echo "Error: Build failed. dist directory not found."
    exit 1
fi

# Create deployment package
echo "Creating deployment package..."
tar -czf dist.tar.gz dist/

# Upload to server with password authentication
echo "Uploading to server (you'll be prompted for password)..."
echo "Password: 'Tew52025!st6@t23GH4B@F%5&k82yU'"
scp dist.tar.gz root@8.211.158.223:/tmp/

if [ $? -ne 0 ]; then
    echo "Error: Failed to upload files to server."
    exit 1
fi

# Deploy on server
echo "Deploying on server..."
echo "You'll be prompted for password again..."
ssh root@8.211.158.223 << 'ENDSSH'
# Install nginx if not present
echo "Installing nginx if needed..."
which nginx || {
    # Try different package managers
    if which yum >/dev/null 2>&1; then
        yum install -y nginx
    elif which apt-get >/dev/null 2>&1; then
        apt-get update && apt-get install -y nginx
    elif which dnf >/dev/null 2>&1; then
        dnf install -y nginx
    else
        echo "Error: No supported package manager found"
        exit 1
    fi
}

# Create web directory for aiedit.hkbu.tech
mkdir -p /var/www/aiedit.hkbu.tech

# Backup existing deployment if it exists
if [ -d "/var/www/aiedit.hkbu.tech/index.html" ]; then
    echo "Backing up existing deployment..."
    cp -r /var/www/aiedit.hkbu.tech /var/www/aiedit.hkbu.tech.backup.$(date +%Y%m%d_%H%M%S)
fi

# Extract files
echo "Extracting new deployment..."
cd /var/www/aiedit.hkbu.tech
tar -xzf /tmp/dist.tar.gz --strip-components=1

# Set proper permissions
chown -R nginx:nginx /var/www/aiedit.hkbu.tech 2>/dev/null || chown -R www-data:www-data /var/www/aiedit.hkbu.tech
chmod -R 755 /var/www/aiedit.hkbu.tech

# Create nginx configuration for aiedit.hkbu.tech
echo "Creating nginx configuration..."
cat > /etc/nginx/conf.d/aiedit.hkbu.tech.conf << 'EOF'
server {
    listen 80;
    server_name aiedit.hkbu.tech www.aiedit.hkbu.tech;
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

    # Poe API proxy (if needed)
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

# Redirect www to non-www
server {
    listen 80;
    server_name www.aiedit.hkbu.tech;
    return 301 http://aiedit.hkbu.tech$request_uri;
}
EOF

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration is valid."

    # Restart nginx
    echo "Restarting nginx..."
    systemctl restart nginx
    systemctl enable nginx

    # Configure firewall
    echo "Configuring firewall..."
    if which firewall-cmd >/dev/null 2>&1; then
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
        echo "Firewall configured with firewalld"
    elif which ufw >/dev/null 2>&1; then
        ufw allow 'Nginx Full'
        echo "Firewall configured with ufw"
    else
        echo "No firewall management tool found. Please manually open ports 80 and 443."
    fi

    echo "✅ Deployment successful!"
    echo "📍 Your WritingBot is now accessible at: http://aiedit.hkbu.tech"
    echo "🔧 Don't forget to set up DNS A record: aiedit.hkbu.tech -> 8.211.158.223"
else
    echo "❌ Nginx configuration test failed. Please check the configuration."
    exit 1
fi

# Cleanup temporary files
rm -f /tmp/dist.tar.gz

echo "🎉 Deployment complete!"
ENDSSH

# Local cleanup
rm -f dist.tar.gz

echo ""
echo "=== Deployment Summary ==="
echo "✅ Built and deployed to: aiedit.hkbu.tech"
echo "🌐 Server IP: 8.211.158.223"
echo ""
echo "📋 Next Steps:"
echo "1. Set up DNS A record in Aliyun CN:"
echo "   aiedit.hkbu.tech -> 8.211.158.223"
echo "2. Wait for DNS propagation (usually 5-10 minutes)"
echo "3. Access your site at: http://aiedit.hkbu.tech"
echo "4. Optional: Set up SSL certificate for HTTPS"
echo ""
echo "🔧 SSL Setup (optional):"
echo "   ssh root@8.211.158.223"
echo "   # Install certbot and get SSL certificate"
echo "   yum install -y certbot python3-certbot-nginx || apt install -y certbot python3-certbot-nginx"
echo "   certbot --nginx -d aiedit.hkbu.tech"
