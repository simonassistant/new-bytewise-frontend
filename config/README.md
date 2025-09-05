# Configuration Management

**Project**: ByteWise Frontend  
**Organization**: Configuration files organized for maintainability  
**Last Updated**: September 5, 2025

---

## 📁 Directory Structure

```
config/
├── deployment/           # Deployment-specific configurations
│   ├── railway.toml     # Railway platform configuration
│   ├── nixpacks.toml    # Nixpacks build configuration  
│   └── .env.production  # Production environment variables
├── serve.json           # Static file serving configuration
└── README.md           # This file
```

**Root Level Symlinks**: 
- `railway.toml` → `config/deployment/railway.toml`
- `nixpacks.toml` → `config/deployment/nixpacks.toml`
- `.env.production` → `config/deployment/.env.production`
- `serve.json` → `config/serve.json`

> **Note**: Symbolic links ensure deployment tools find configs in expected locations while keeping files organized.

---

## 🚀 Deployment Configuration

### Railway Configuration (`deployment/railway.toml`)
- **Purpose**: Railway platform settings, health checks, restart policies
- **Node Version**: 20.19.0 (required for Vite 7.x)
- **Health Check**: `healthcheckPath = "/"`
- **Restart Policy**: On failure with 10 max retries

### Nixpacks Configuration (`deployment/nixpacks.toml`)  
- **Purpose**: Explicit build process configuration
- **Build Steps**: setup → install → build → start
- **Package Manager**: npm with `npm ci` for production installs

### Environment Variables (`deployment/.env.production`)
- **Purpose**: Production environment settings
- **API URLs**: Backend service endpoints
- **Domain**: Custom domain configuration
- **Node Environment**: Production-specific settings

### Static Serving (`serve.json`)
- **Purpose**: SPA routing configuration for serve package
- **Rewrites**: All routes redirect to `/index.html` for Vue Router

---

## 🔧 Configuration Guidelines

### For Deployment Changes
1. **Edit files in `config/` directory**
2. **Test changes locally** with `npm run railway:build`
3. **Commit changes** - symlinks will automatically reflect updates
4. **Deploy** - Railway will detect configuration changes

### For Environment Variables
1. **Development**: Use `.env.local` (gitignored)
2. **Production**: Update `config/deployment/.env.production`
3. **Railway**: Set additional variables in Railway dashboard

### For New Configuration Files
1. **Add to appropriate subdirectory** in `config/`
2. **Create symlink if needed** for tool compatibility
3. **Document purpose and usage** in this README
4. **Update .gitignore** if necessary

---

## 📋 Configuration Checklist

### Before Deployment
- [ ] All config files valid syntax
- [ ] Environment variables set correctly
- [ ] Node.js version compatible (20.19.0+)
- [ ] Health check endpoints accessible
- [ ] Static file serving configured

### After Configuration Changes
- [ ] Local build successful (`npm run railway:build`)
- [ ] Symlinks point to correct files
- [ ] No sensitive data in version control
- [ ] Documentation updated
- [ ] Team notified of changes

---

## 🔍 Troubleshooting

### Common Issues
1. **Symlink broken**: Re-create with `ln -sf target link`
2. **Railway can't find config**: Check symlinks in root directory
3. **Build fails**: Verify Node.js version in configurations
4. **Environment variables not loaded**: Check file location and syntax

### Validation Commands
```bash
# Check symlinks
ls -la *.toml *.json .env.production

# Validate Railway config
railway validate  # (if Railway CLI installed)

# Test build process
npm run railway:build
```

---

## 🔐 Security Notes

- **Sensitive Data**: Never commit API keys or secrets to git
- **Environment Files**: Use Railway dashboard for production secrets
- **Access Control**: Limit who can modify deployment configurations
- **Backup**: Keep backup of working configurations before major changes

---

*Configuration organized for maintainability and team collaboration*  
*For questions about specific configs, see deployment documentation*
