# DNS Setup Guide for aiedit.hkbu.tech

## Prerequisites
- You own the domain `hkbu.tech`
- You have access to Aliyun CN domain management
- Your server IP is `8.211.158.223`

## Steps to Set Up DNS

### 1. Log into Aliyun CN Console
1. Go to [Aliyun CN Console](https://ecs.console.aliyun.com/)
2. Navigate to \"Domain\" or \"域名\" section
3. Find your `hkbu.tech` domain

### 2. Add DNS Record
1. Click on \"Resolve\" or \"解析\" for `hkbu.tech`
2. Add a new A record:
   - **Host Record (主机记录)**: `aiedit`
   - **Record Type (记录类型)**: `A`
   - **Record Value (记录值)**: `8.211.158.223`
   - **TTL**: `600` (10 minutes)

### 3. Optional: Add WWW Subdomain
Add another A record:
- **Host Record**: `www.aiedit`
- **Record Type**: `A`
- **Record Value**: `8.211.158.223`
- **TTL**: `600`

### 4. Verify DNS Propagation
After 5-10 minutes, test with:
```bash
nslookup aiedit.hkbu.tech
ping aiedit.hkbu.tech
```

## Alternative: Use Aliyun CDN (Recommended for China)

If you want better performance in China:

1. Set up Aliyun CDN for `aiedit.hkbu.tech`
2. Point CDN origin to `8.211.158.223`
3. Configure CNAME record instead of A record

## SSL Certificate Setup (After DNS)

Once DNS is working, set up HTTPS:

```bash
ssh root@8.211.158.223

# Install certbot
yum install -y certbot python3-certbot-nginx
# or for Ubuntu: apt install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d aiedit.hkbu.tech -d www.aiedit.hkbu.tech

# Set up auto-renewal
echo \"0 12 * * * /usr/bin/certbot renew --quiet\" | crontab -
```

## Firewall Configuration (if needed)

```bash
# For Aliyun Security Groups
# 1. Go to ECS Console
# 2. Security Groups
# 3. Add rules for ports 80 and 443

# For server firewall
ssh root@8.211.158.223
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

## Testing Checklist

- [ ] DNS A record created: `aiedit.hkbu.tech -> 8.211.158.223`
- [ ] DNS propagation complete (nslookup works)
- [ ] Website accessible via http://aiedit.hkbu.tech
- [ ] SSL certificate installed (if desired)
- [ ] Website accessible via https://aiedit.hkbu.tech
- [ ] All features working (WritingBot, Poe integration, etc.)

## Troubleshooting

### DNS Not Resolving
- Wait longer (up to 24 hours for full propagation)
- Check DNS settings in Aliyun console
- Use different DNS servers for testing

### Website Not Loading
- Check nginx status: `systemctl status nginx`
- Check nginx error logs: `tail -f /var/log/nginx/error.log`
- Verify server is running: `ping 8.211.158.223`

### SSL Issues
- Ensure DNS is fully propagated before running certbot
- Check nginx configuration: `nginx -t`
- Review certbot logs: `tail -f /var/log/letsencrypt/letsencrypt.log`
