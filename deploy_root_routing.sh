#!/bin/bash

# Deploy script for root routing update
echo "🚀 Deploying new-bytewise-frontend with root routing to Aliyun server..."

# Create a tarball of the dist directory
echo "📦 Creating deployment package..."
tar -czf root_routing_deployment.tar.gz dist/

# Upload the tarball to the server
echo "⬆️ Uploading files to server..."
scp root_routing_deployment.tar.gz root@8.211.158.223:/tmp/

# Execute deployment commands on the server
echo "🔧 Deploying on server..."
ssh root@8.211.158.223 << 'EOF'
    # Navigate to web directory
    cd /var/www/aiedit.hkbu.tech

    # Backup current deployment
    if [ -d "dist_backup" ]; then
        rm -rf dist_backup
    fi
    if [ -d "dist" ]; then
        mv dist dist_backup
    fi

    # Extract new deployment
    tar -xzf /tmp/root_routing_deployment.tar.gz

    # Set proper permissions
    chown -R www-data:www-data dist/
    chmod -R 755 dist/

    # Clean up
    rm /tmp/root_routing_deployment.tar.gz

    # Restart nginx to ensure changes take effect
    systemctl reload nginx

    echo "✅ Deployment completed successfully!"
    echo "🌐 Site should be accessible at http://aiedit.hkbu.tech/"
EOF

# Clean up local tarball
rm root_routing_deployment.tar.gz

echo "🎉 Deployment process completed!"
echo "🌐 Your WritingBot should now be accessible at http://aiedit.hkbu.tech/"
echo "📝 The old /writingbot path will redirect to the root automatically"
