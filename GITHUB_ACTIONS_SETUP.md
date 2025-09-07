# 🚀 GitHub Actions Railway Deployment Setup

## 📋 **What This GitHub Action Does**

✅ **Automatic deployment** when code is pushed to `main` branch  
✅ **Build verification** on pull requests  
✅ **Manual deployment trigger** via GitHub UI  
✅ **Staging deployment** with `[staging]` in commit message  
✅ **Environment variable management**  
✅ **Deployment status notifications**  

## 🔐 **Required GitHub Secrets Setup**

Bob needs to add these secrets to his GitHub repository:

### **Step 1: Get Railway Token**
```bash
# Bob runs this in terminal:
railway login
railway auth

# Or get from Railway dashboard:
# Settings → Tokens → Create New Token
```

### **Step 2: Get Railway Project IDs**
```bash
# Bob runs this to get project IDs:
railway list
railway link --project "Your Project Name"
railway status  # Shows project ID
```

### **Step 3: Add GitHub Secrets**
Go to `Bob8259/new-bytewise-frontend` → Settings → Secrets and variables → Actions

**Add these secrets:**

| Secret Name | Value | Description |
|-------------|--------|-------------|
| `RAILWAY_TOKEN` | `your-railway-token-here` | Railway API token |
| `RAILWAY_PROJECT_ID` | `project-id-for-production` | Main production project ID |
| `RAILWAY_STAGING_PROJECT_ID` | `project-id-for-staging` | Staging/test project ID (optional) |

## 🚀 **How to Use**

### **Automatic Deployment:**
```bash
git push origin main
# → Triggers automatic deployment to production
```

### **Staging Deployment:**
```bash
git commit -m "New feature [staging]"
git push origin main
# → Triggers staging deployment
```

### **Manual Deployment:**
- Go to GitHub → Actions tab
- Select "🚀 Deploy to Railway"
- Click "Run workflow"

## 🎯 **Workflow Triggers**

| Trigger | Action | Environment |
|---------|---------|-------------|
| Push to `main` | Auto-deploy | Production |
| Pull Request | Build & Test | Test only |
| Commit with `[staging]` | Deploy | Staging |
| Manual trigger | Deploy | Production |
| Ignore paths | Skip | Docs, README |

## 📁 **File Structure Created**

```
.github/
└── workflows/
    └── railway-deploy.yml     # Main deployment workflow
```

## ⚙️ **Environment Variables Auto-Set**

The GitHub Action automatically configures:

**Production:**
```env
NODE_ENV=production
VITE_APP_DOMAIN=https://avatartutor.hkbu.tech
VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api
VITE_APP_TITLE=ByteWise Avatar Tutor
```

**Staging:**
```env
NODE_ENV=staging
VITE_APP_DOMAIN=https://avatar-test.hkbu.tech
VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api
VITE_APP_TITLE=ByteWise Avatar Tutor (Test)
```

## 🔍 **Deployment Process**

1. **Code pushed** to main branch
2. **GitHub Action triggers** automatically
3. **Dependencies installed** with npm ci
4. **Environment variables** set via Railway CLI
5. **Build and deploy** via `railway up`
6. **Status verification** and notifications

## 📊 **Monitoring Deployments**

### **GitHub Interface:**
- Go to repository → Actions tab
- View deployment logs and status
- See success/failure notifications

### **Railway Interface:**
- Monitor deployment progress
- View application logs
- Check domain status

## 🔧 **Advanced Features**

### **Environment Protection:**
- Production deployments require approval (optional)
- Staging deployments are automatic
- Manual deployment override available

### **Build Optimization:**
- Node.js caching for faster builds
- Skip deployment on documentation changes
- Parallel build and test jobs

### **Error Handling:**
- Deployment failure notifications
- Automatic status checks
- Rollback capabilities

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **Railway Token Invalid:**
   - Generate new token in Railway dashboard
   - Update GitHub secret

2. **Project ID Wrong:**
   - Run `railway status` to get correct ID
   - Update GitHub secret

3. **Environment Variables:**
   - Check Railway dashboard for variable conflicts
   - Verify API URLs are correct

### **Debug Commands:**
```bash
# Check Railway CLI
railway whoami
railway status

# Verify project linking
railway list
railway link --project "Project Name"
```

## ✅ **Testing the Setup**

### **Test 1: Automatic Deployment**
```bash
echo "# Test deployment" >> README.md
git add .
git commit -m "Test GitHub Actions deployment"
git push origin main
```

### **Test 2: Manual Deployment**
1. Go to GitHub Actions
2. Select workflow
3. Click "Run workflow"

### **Test 3: Staging Deployment**
```bash
git commit -m "Test staging deployment [staging]"
git push origin main
```

## 📈 **Benefits for Bob**

✅ **Zero manual deployment** - Push code, get deployment  
✅ **No CLI setup required** - Everything in GitHub  
✅ **Visual deployment history** - See all deployments in GitHub  
✅ **Automatic rollback** - Easy to revert to previous versions  
✅ **Environment management** - Production vs staging automatic  
✅ **Team collaboration** - Anyone can see deployment status  

---

**Next Steps for Bob:**
1. Add the GitHub secrets
2. Push code to main branch  
3. Watch the automatic deployment! 🚀
