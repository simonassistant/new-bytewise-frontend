# Railway Testing Environment Setup

**Environment**: Testing/Staging  
**Domain**: https://avatar-test.hkbu.tech/  
**Repository**: `tesolchina/new-bytewise-frontend`  
**Branch**: `feature/development-work` (or `main` for stable testing)  
**Purpose**: Safe testing environment for development work

---

## 🎯 **Testing Environment Purpose**

This testing environment allows you to:
- ✅ **Test new features** before deploying to production
- ✅ **Validate Railway deployments** work correctly
- ✅ **Share work-in-progress** with team members
- ✅ **Debug issues** without affecting production users
- ✅ **Practice deployment process** before production releases

---

## 🚀 **Railway Testing Project Setup**

### **Step 1: Create New Railway Project**

1. **Go to Railway Dashboard**: https://railway.app/dashboard
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose Repository**: `tesolchina/new-bytewise-frontend`
5. **Select Branch**: `feature/development-work` (or `main` for stable testing)
6. **Project Name**: `bytewise-frontend-testing`

### **Step 2: Environment Variables**

Set these in Railway dashboard under "Variables":

```bash
NODE_ENV=staging
VITE_APP_TITLE=ByteWise Avatar Tutor (Testing)
VITE_APP_DOMAIN=https://avatar-test.hkbu.tech
VITE_API_BASE_URL=https://new-bytewise-backend-production-8c33.up.railway.app/api
VITE_TESTING_MODE=true
VITE_ENABLE_DEBUG=true
```

### **Step 3: Custom Domain Setup**

1. **In Railway Project**: Go to "Settings" → "Domains"
2. **Add Custom Domain**: `avatar-test.hkbu.tech`
3. **Copy CNAME Target**: Railway will provide a domain like `bytewise-frontend-testing-production-xxxx.up.railway.app`

### **Step 4: DNS Configuration (Alibaba Cloud)**

1. **Login to Alibaba Cloud**: https://cn.aliyun.com/
2. **Domain Management**: Find your `hkbu.tech` domain
3. **Add CNAME Record**:
   - **Host**: `avatar-test`
   - **Type**: `CNAME`
   - **Value**: `[railway-generated-domain]` (from step 3 above)
   - **TTL**: `600` (10 minutes)

---

## 🔧 **Development Workflow with Testing**

### **Testing New Features**

```bash
# Work on feature branch
git checkout feature/new-feature-name

# Make your changes and test locally
npm run dev

# Build and test Railway deployment
npm run railway:build

# Push to your fork
git push origin feature/new-feature-name
```

**Railway will automatically deploy** from your pushed branch to https://avatar-test.hkbu.tech/

### **Testing Branch Strategy**

- **`feature/development-work`**: Main development branch, continuously deployed to testing
- **`feature/specific-feature`**: Specific feature branches, deployed when needed
- **`main`**: Stable branch, can be used for stable testing before production

### **Promoting to Production**

Once testing is successful:

```bash
# Switch to main branch
git checkout main

# Merge tested features
git merge feature/development-work

# Push to main
git push origin main

# Create PR to Bob's repository
# Deploy to production (avatar.hkbu.tech) after PR approval
```

---

## 🧪 **Testing Checklist**

### **Before Each Deployment Test**

- [ ] **Local testing** passes (`npm run dev`)
- [ ] **Build succeeds** (`npm run railway:build`)
- [ ] **Feature branch** pushed to fork
- [ ] **Railway detects** and starts deployment

### **After Deployment to Testing**

- [ ] **Site loads** at https://avatar-test.hkbu.tech/
- [ ] **New features** work as expected
- [ ] **Existing features** still functional (no regressions)
- [ ] **API connections** working correctly
- [ ] **Mobile responsiveness** verified
- [ ] **Cross-browser** compatibility checked

### **Voice/Avatar Features Testing**

- [ ] **Microphone access** prompts correctly
- [ ] **Speech-to-text** functionality works
- [ ] **Audio playback** from AI responses
- [ ] **WebSocket connections** stable
- [ ] **Error handling** graceful

### **Performance Testing**

- [ ] **Page load speed** acceptable
- [ ] **Bundle size** optimized
- [ ] **Memory usage** reasonable during long sessions
- [ ] **Token counter** updates correctly

---

## 🔍 **Testing Environment Differences**

### **vs. Local Development**
- **Environment**: `staging` vs `development`
- **Build**: Production build vs development build
- **API**: Real backend vs potentially local backend
- **Domain**: https vs http (SSL certificate testing)

### **vs. Production**
- **Domain**: `avatar-test.hkbu.tech` vs `avatartutor.hkbu.tech`
- **Branch**: Feature branch vs main branch
- **Data**: Testing data vs production data
- **Users**: Development team vs real users

---

## 🚨 **Testing Best Practices**

### **Feature Testing**
1. **Test thoroughly** before pushing
2. **Document test results** in development logs
3. **Check all user flows** end-to-end
4. **Verify API integrations** work correctly
5. **Test edge cases** and error conditions

### **Deployment Testing**
1. **Monitor Railway logs** during deployment
2. **Check for build errors** or warnings
3. **Verify environment variables** loaded correctly
4. **Test immediately** after deployment completes
5. **Rollback quickly** if major issues found

### **Team Communication**
1. **Announce** when testing environment updated
2. **Share test results** with team members
3. **Document issues** found during testing
4. **Coordinate** testing activities to avoid conflicts

---

## 📊 **Monitoring & Debugging**

### **Railway Dashboard**
- **Deployment Logs**: Check for build and runtime errors
- **Metrics**: Monitor CPU, memory, and request usage
- **Health Checks**: Ensure application stays healthy

### **Browser Developer Tools**
- **Console**: Check for JavaScript errors
- **Network**: Monitor API calls and performance
- **Application**: Verify service worker and storage

### **Testing-Specific Debugging**
```javascript
// Use testing environment variables for debugging
if (import.meta.env.VITE_TESTING_MODE === 'true') {
  console.log('Testing mode enabled');
}

if (import.meta.env.VITE_ENABLE_DEBUG === 'true') {
  // Enable additional logging
}
```

---

## 🎯 **Success Criteria**

### **Testing Environment Ready When**
- [ ] Railway project deploys successfully
- [ ] Custom domain `avatar-test.hkbu.tech` accessible
- [ ] All core features working
- [ ] Environment variables configured correctly
- [ ] DNS propagation complete
- [ ] SSL certificate active
- [ ] No console errors or warnings

### **Ready for Production When**
- [ ] All features tested and working in testing environment
- [ ] Performance acceptable
- [ ] No regressions in existing functionality
- [ ] User acceptance testing completed
- [ ] Team approval for production deployment

---

*Testing environment setup - safe space for development and validation*
