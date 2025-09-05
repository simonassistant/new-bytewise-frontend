# Development Collaboration Guide

**Project**: ByteWise Frontend  
**Team**: tesolchina (fork maintainer) + Bob8259 (original maintainer)  
**Updated**: September 5, 2025

---

## 🎯 Collaboration Workflow

### Repository Structure
- **Main Repository**: `Bob8259/new-bytewise-frontend` (upstream)
- **Development Fork**: `tesolchina/new-bytewise-frontend` (origin)
- **Collaboration Method**: Fork-based development with pull requests

### Branch Strategy
```
main (production-ready)
├── feature/feature-name (development branches)
├── fix/bug-description (bug fixes)
├── enhancement/improvement-name (enhancements)
└── docs/documentation-updates (documentation only)
```

---

## 📋 Development Process

### 1. **Starting New Work**
```bash
# Ensure you're on main and up-to-date
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# Create feature branch
git checkout -b feature/descriptive-name
```

### 2. **During Development**
- **Document as you go**: Add entries to development log
- **Test locally**: Use `npm run dev` and `npm run build`
- **Commit frequently**: Small, focused commits with clear messages
- **Update documentation**: Keep docs current with changes

### 3. **Before Submitting PR**
```bash
# Final testing
npm run build
npm run railway:build

# Update development log
# See docs/collaboration/DEVELOPMENT_LOG_TEMPLATE.md

# Push to fork
git push origin feature/your-branch-name
```

### 4. **Pull Request Process**
1. **Create PR** from your fork to Bob's main repository
2. **Fill out PR template** (see `.github/pull_request_template.md`)
3. **Link related issues** if applicable
4. **Request review** from Bob8259
5. **Address feedback** promptly
6. **Merge** after approval

---

## 📊 Development Documentation Standards

### Daily Development Log
**Location**: `logs/development-log-YYYY-MM-DD.md`

**Required Sections**:
- **Session Overview**: What you worked on
- **Changes Made**: Files modified, features added
- **Testing Results**: What you tested and results
- **Issues Encountered**: Problems and solutions
- **Next Steps**: What to work on next

### Feature Documentation
**Location**: `docs/development/feature-name.md`

**Required for major features**:
- Feature description and goals
- Technical implementation details  
- Testing approach and results
- Deployment considerations
- User impact assessment

### Bug Fix Documentation
**Location**: `logs/bugfix-YYYY-MM-DD-issue-description.md`

**Required sections**:
- Problem description
- Root cause analysis
- Solution implemented
- Testing verification
- Prevention measures

---

## 🔄 Communication Protocols

### For Major Changes
1. **Create GitHub Issue** in Bob's repository first
2. **Discuss approach** in issue comments
3. **Create development branch** after agreement
4. **Regular updates** in PR comments

### For Minor Changes
1. **Create branch** directly
2. **Document in commit messages**
3. **Submit PR** with clear description

### For Questions/Discussions
1. **GitHub Discussions** in Bob's repository
2. **Issue comments** for specific problems
3. **PR comments** for code-specific questions

---

## 🧪 Testing Requirements

### Before Every Commit
- [ ] Code builds successfully (`npm run build`)
- [ ] No console errors in development (`npm run dev`)
- [ ] Features work as expected locally

### Before Every PR
- [ ] Railway build succeeds (`npm run railway:build`)
- [ ] All existing features still work
- [ ] New features are documented
- [ ] Development log is updated

### For Major Features
- [ ] Cross-browser testing
- [ ] Mobile responsiveness verified
- [ ] Voice features tested (if applicable)
- [ ] Email functionality verified (if applicable)
- [ ] Performance impact assessed

---

## 📝 Documentation Maintenance

### Keep Updated
- Development logs after each session
- Feature documentation for new features
- Deployment guides when process changes
- This collaboration guide when workflow evolves

### Review Regularly
- Monthly review of documentation accuracy
- Quarterly review of collaboration process effectiveness
- Update templates and guides based on experience

---

## 🚨 Emergency Procedures

### Critical Bug in Production
1. **Create hotfix branch** from main
2. **Fix issue** with minimal changes
3. **Test thoroughly**
4. **Submit PR** marked as "URGENT"
5. **Document** in emergency log

### Deployment Issues
1. **Check Railway logs** first
2. **Revert to last working commit** if needed
3. **Document issue** in deployment log
4. **Fix and redeploy** once issue is identified

---

## 🎯 Quality Standards

### Code Quality
- Clear, descriptive variable names
- Proper Vue.js component structure
- Consistent formatting (Prettier recommended)
- Comments for complex logic

### Documentation Quality
- Clear, actionable instructions
- Up-to-date information
- Examples where helpful
- Proper markdown formatting

### Commit Quality
- Descriptive commit messages
- Atomic commits (one logical change per commit)
- Conventional commit format preferred:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code refactoring

---

## 🏆 Success Metrics

### Development Velocity
- Features completed per week
- Bug fix turnaround time
- PR review and merge time

### Code Quality
- Build success rate
- Number of post-deployment issues
- User-reported bugs

### Collaboration Effectiveness
- PR approval rate
- Communication clarity
- Documentation completeness

---

*This guide evolves with our development process. Suggest improvements via GitHub issues or PR comments.*
