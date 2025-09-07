# 🚂 Railway Deployment Records

**Last Updated:** September 7, 2025
**Account:** Simon Wang (simonwang@hkbu.edu.hk)

---

## 📊 **All Railway Projects Overview**

### **Active Projects:**

1. **HKBU LC chatbot(unofficial)**
2. **Test Avatar Tutor** ⭐ *Current Working Project*
3. **proactive-blessing**
4. **noble-caring**
5. **zucchini-reprieve**
6. **precious-mercy**
7. **romantic-beauty**
8. **cozy-upliftment**
9. **striking-tranquility**
10. **spirited-energy**

---

## 🎯 **Detailed Project Information**

### **1. Test Avatar Tutor** ⭐

**Status:** ✅ Active (Current Working Project)
**Environment:** Production
**Service:** Test Avatar Tutor
**Domain:** https://avatar-test.hkbu.tech
**GitHub Repository:** https://github.com/tesolchina/new-bytewise-frontend
**Branch:** feature/development-work
**Technology:** Vue 3 + Vite + Railway
**Purpose:** ByteWise AI Chatbot with iFrame embedding capabilities

**Deployment Details:**

- **Build Command:** `npm run railway:build` (npm run build)
- **Start Command:** `npm run railway:start` (serve -s dist -p $PORT)
- **Node Version:** 20.19.0
- **Builder:** Nixpacks
- **Health Check:** `/` (300s timeout)

### **2. HKBU LC chatbot(unofficial)**

**Status:** ✅ Active
**Environment:** Production
**Service:** HKBU LC chatbot(unofficial)
**Domain:** https://hkbu-lc-chatbotunofficial-production.up.railway.app
**GitHub Repository:** Unknown (need to check)
**Technology:** Unknown (need to check)
**Purpose:** HKBU LC Chatbot (Unofficial)

### **3. proactive-blessing**

**Status:** ✅ Active
**Environment:** Production
**Service:** new-bytewise-frontend
**Domain:** https://avatartutor.hkbu.tech
**GitHub Repository:** Unknown (need to check)
**Technology:** Unknown (need to check)
**Purpose:** Avatar Tutor

### **4. zucchini-reprieve**

**Status:** ✅ Active
**Environment:** Production
**Service:** new-bytewise-backend
**Domain:** https://new-bytewise-backend-production-8c33.up.railway.app
**GitHub Repository:** Unknown (likely Bob8259/new-bytewise-backend)
**Technology:** Backend API (likely Node.js/Python)
**Purpose:** ByteWise Backend API Service

---

## 🔗 **Domain Mapping**

| Domain                                                          | Project                     | Status    | Notes                       |
| --------------------------------------------------------------- | --------------------------- | --------- | --------------------------- |
| `https://avatar-test.hkbu.tech`                               | Test Avatar Tutor           | ✅ Active | Current development project |
| `https://hkbu-lc-chatbotunofficial-production.up.railway.app` | HKBU LC chatbot(unofficial) | ✅ Active | Railway default domain      |
| `https://avatartutor.hkbu.tech`                               | proactive-blessing          | ✅ Active | Custom domain               |
| `https://new-bytewise-backend-production-8c33.up.railway.app` | zucchini-reprieve           | ✅ Active | Backend API service         |

---

## 📝 **GitHub Repository Mapping**

| Project                     | GitHub Repository                         | Branch                       | Status                |
| --------------------------- | ----------------------------------------- | ---------------------------- | --------------------- |
| Test Avatar Tutor           | `tesolchina/new-bytewise-frontend`      | `feature/development-work` | ✅ Active Development |
| HKBU LC chatbot(unofficial) | Unknown                                   | Unknown                      | ❓ Need to verify     |
| proactive-blessing          | Unknown                                   | Unknown                      | ❓ Need to verify     |
| zucchini-reprieve           | `Bob8259/new-bytewise-backend` (likely) | Unknown                      | ❓ Need to verify     |


let's do the avatar and text-based chatbot development separately 

avatartutor.hkbu.tech is still linked to https://github.com/Bob8259/new-bytewise-frontend 


aitutor.hkbu.tech will be linked to https://github.com/tesolchina/AItutor_text which will be texts-based customised chatbot (no speech or video supported) 






## 🏗️ **Deployment Configuration**

### **Test Avatar Tutor - Current Project**

```toml
[build]
builder = "NIXPACKS"
watchPatterns = ["**/*.vue", "**/*.js", "**/*.ts", "**/*.json", "**/*.md"]

[deploy]
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[variables]
NODE_VERSION = "20.19.0"
```

**Package.json Scripts:**

```json
{
  "scripts": {
    "railway:build": "npm run build",
    "railway:start": "serve -s dist -p $PORT"
  }
}
```

---

## 🔍 **Investigation Needed**

### **Projects Requiring Further Investigation:**

1. **HKBU LC chatbot(unofficial)**

   - Check GitHub repository linkage
   - Verify technology stack
   - Review deployment configuration
2. **proactive-blessing**

   - Check GitHub repository linkage
   - Verify technology stack
   - Review deployment configuration
3. **Remaining Projects (noble-caring, zucchini-reprieve, etc.)**

   - Check if these are active or archived
   - Verify their purpose and GitHub linkage

---

## 📋 **Management Commands**

### **Check Current Project Status:**

```bash
railway status
```

### **View Domains:**

```bash
railway domain
```

### **List All Projects:**

```bash
railway list
```

### **Link to Specific Project:**

```bash
railway link --project "Project Name"
```

### **View Logs:**

```bash
railway logs
```

### **Redeploy:**

```bash
railway redeploy
```

---

## 🎯 **Current Working Context**

**Active Project:** Test Avatar Tutor
**Domain:** https://avatar-test.hkbu.tech
**GitHub:** tesolchina/new-bytewise-frontend
**Branch:** feature/development-work
**Status:** 🚀 Complete iFrame Embeddable Architecture & Context Analysis

**Recent Work:**

- ✅ Phase 2: iFrame Implementation Architecture
- ✅ Phase 4.1: Context Memory Enhancement Analysis
- 📝 Ready for Phase 4.2: Enhanced Context Management Implementation

---

## 📞 **Support & Contact**

**Railway Account:** Simon Wang (simonwang@hkbu.edu.hk)
**GitHub:** tesolchina (Primary) / Bob8259 (Reference)
**Current Focus:** ByteWise AI Chatbot iFrame Embedding

---

*This document serves as a comprehensive record of all Railway deployments and their associated domains and GitHub repositories. Update this document whenever new projects are deployed or existing ones are modified.*
