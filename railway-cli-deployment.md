# Railway CLI Deployment Strategy

## 🔄 Transition from GUI to CLI

### Current Projects (via CLI):
- **New Bytewise Backend** - Backend service
- **Avatartutor.hkbu.tech** - Main frontend deployment
- **aitutor.hkbu.tech** - Alternative frontend
- **Test Avatar Tutor** - Testing environment

## 🛠 CLI Deployment Workflow

### 1. Project Linking & Environment Setup
```bash
# Link to specific project
railway link --project "Avatartutor.hkbu.tech"

# Set environment variables via CLI
railway variables set NODE_ENV=production
railway variables set VITE_APP_DOMAIN=https://avatartutor.hkbu.tech
railway variables set VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api

# List current variables
railway variables list
```

### 2. Automated Deployment Script
```bash
#!/bin/bash
# deploy.sh - Automated Railway deployment

echo "🚀 Starting Railway CLI deployment..."

# Ensure we're on the right project
railway link --project "Avatartutor.hkbu.tech"

# Deploy current branch
railway up

# Check deployment status
railway status

# View logs
railway logs --tail
```

### 3. Domain Management via CLI
```bash
# List current domains
railway domain

# Add custom domain (if needed)
railway domain add avatartutor.hkbu.tech

# Remove domain
railway domain remove old-domain.com
```

### 4. Service Configuration
```bash
# View current service info
railway service

# Check deployment logs
railway logs --lines 100

# Restart service
railway restart
```

## 📋 Migration Steps from GUI to CLI

### Phase 1: CLI Setup (✅ Done)
- [x] Railway CLI installed
- [x] Authentication completed
- [x] Projects visible via CLI

### Phase 2: Configuration Migration
```bash
# 1. Export current environment variables from GUI
railway variables list > current-env.txt

# 2. Backup current railway.toml
cp railway.toml railway.toml.backup

# 3. Update railway.toml for CLI optimization
```

### Phase 3: Automated Deployment Pipeline
```bash
# Create deployment script
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "🔍 Checking Railway CLI status..."
railway whoami

echo "🔗 Linking to project..."
railway link --project "Avatartutor.hkbu.tech"

echo "📦 Building and deploying..."
railway up --detach

echo "✅ Deployment initiated!"
railway logs --tail
EOF

chmod +x deploy.sh
```

## 🎯 CLI Advantages Over GUI

### **GUI Limitations:**
- Manual clicking for each deployment
- No version control for configuration
- Difficult to replicate across environments
- No batch operations

### **CLI Benefits:**
- **Scriptable deployments**: `./deploy.sh`
- **Version controlled**: All commands in git
- **Batch operations**: Update multiple services
- **Automation ready**: CI/CD integration

## 🚀 Recommended CLI Workflow

### Daily Development:
```bash
# Quick deploy current branch
railway up

# Monitor logs
railway logs --tail

# Check status
railway status
```

### Environment Management:
```bash
# Production deployment
railway link --project "Avatartutor.hkbu.tech"
railway variables set NODE_ENV=production
railway up

# Testing deployment  
railway link --project "Test Avatar Tutor"
railway variables set NODE_ENV=staging
railway up
```

### Domain Operations:
```bash
# Check all domains
railway domain

# Add new domain
railway domain add new-domain.hkbu.tech

# Update DNS (manual step in Alibaba Cloud)
```

## 📊 CLI Commands Cheat Sheet

| Operation | CLI Command | GUI Alternative |
|-----------|-------------|-----------------|
| Deploy | `railway up` | Manual trigger in dashboard |
| Variables | `railway variables set KEY=value` | Environment tab |
| Logs | `railway logs --tail` | Logs tab |
| Domains | `railway domain` | Settings → Domains |
| Status | `railway status` | Project overview |
| Restart | `railway restart` | Manual restart button |

## ⚡ Next Steps

1. **Test CLI deployment**: `railway up` from current branch
2. **Create deployment script**: Automate the process
3. **Update documentation**: Include CLI commands
4. **Train team**: Share CLI workflow with collaborators

Would you like me to create the automated deployment script and test the CLI deployment process?
