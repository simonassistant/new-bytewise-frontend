# Sprint 1: Foundation & Layout

**Sprint Duration**: September 5-19, 2025 (2 weeks)
**Sprint Goal**: Create the basic infrastructure for animated avatar and WeChat-style chat layout
**Theme**: "Setting the Stage"

---

## 🎯 **Sprint Objectives**

### **Primary Goals**

1. **Avatar Panel Infrastructure** - Side panel that can show/hide the animated avatar
2. **WeChat-Style Chat Layout** - Transform existing chat into bubble conversations
3. **Input Mode Toggle** - Switch between typing and voice input modes

### **Success Criteria**

- [ ] Side panel slides in/out smoothly with toggle button
- [ ] Chat messages display as bubbles with avatars (WeChat style)
- [ ] Users can switch between keyboard and microphone input modes
- [ ] All features work responsively on mobile and desktop
- [ ] No regressions to existing functionality

---

## 📋 **Sprint Backlog**

### **🏗️ Story 1.1: Avatar Panel Infrastructure**

**Story Points**: 8 | **Priority**: Must Have | **Assignee**: Developer

#### **Description**

Create a collapsible side panel where the animated avatar will live. This panel should slide in/out smoothly and not interfere with the existing chat functionality.

#### **Acceptance Criteria**

- [ ] Side panel component created (`AvatarPanel.vue`)
- [ ] Panel slides in from right with 300ms ease animation
- [ ] Toggle button (💬→🎭) to show/hide panel
- [ ] Panel width: 320px on desktop, full overlay on mobile (<768px)
- [ ] Panel state persisted in localStorage (`avatarPanelVisible`)
- [ ] Panel doesn't push main content (overlay style)
- [ ] Z-index properly layered above main content

#### **Technical Tasks**

- [ ] Create `src/components/avatar/AvatarPanel.vue`
- [ ] Add panel toggle button to main navigation
- [ ] Implement slide animation with CSS transforms
- [ ] Add responsive breakpoints for mobile behavior
- [ ] Set up localStorage for persistence
- [ ] Add proper z-index layering

#### **Definition of Done**

- [ ] Panel slides in/out smoothly on both desktop and mobile
- [ ] Toggle state persists across page refreshes
- [ ] No layout shifts or interference with existing chat
- [ ] Code reviewed and meets quality standards

---

### **💬 Story 1.2: WeChat-Style Chat Layout**

**Story Points**: 13 | **Priority**: Must Have | **Assignee**: Developer

#### **Description**

Transform the existing linear chat interface into a WeChat-style bubble conversation layout with user messages on the right (blue) and AI messages on the left (gray).

#### **Acceptance Criteria**

- [ ] Chat bubble component created (`ChatBubble.vue`)
- [ ] User messages: right-aligned, blue bubbles with user avatar
- [ ] AI messages: left-aligned, gray bubbles with AI avatar/icon
- [ ] Message timestamps shown on hover
- [ ] Smooth bubble appearance: fade-in + slide animation (200ms)
- [ ] Auto-scroll to newest message
- [ ] Proper spacing between message groups
- [ ] Responsive bubbles adapt to screen width

#### **Technical Tasks**

- [ ] Create `src/components/avatar/ChatBubble.vue`
- [ ] Update `src/views/Chat.vue` to use bubble layout
- [ ] Add message type detection (user/ai)
- [ ] Implement bubble animations (CSS keyframes)
- [ ] Add auto-scroll functionality
- [ ] Create responsive bubble width constraints
- [ ] Add hover effects for timestamps

#### **Definition of Done**

- [ ] All existing messages display as styled bubbles
- [ ] Message flow feels natural and conversational
- [ ] Animations are smooth and not jarring
- [ ] Mobile experience is optimized
- [ ] Backwards compatibility with existing chat data

---

### **🔄 Story 1.3: Input Mode Toggle System**

**Story Points**: 5 | **Priority**: Must Have | **Assignee**: Developer

#### **Description**

Create a toggle system that allows users to switch between typing mode (keyboard input) and voice mode (microphone input), with the UI adapting based on the selected mode.

#### **Acceptance Criteria**

- [ ] Toggle component created (`InputModeToggle.vue`)
- [ ] Visual toggle: ⌨️ Typing ⇄ 🎤 Voice
- [ ] Toggle switch animates between states
- [ ] Input area changes based on mode:
  - Typing: Traditional text input with send button
  - Voice: Microphone button with status indicator
- [ ] Current mode stored in localStorage
- [ ] Mode preference restored on page load
- [ ] Clear visual indication of current active mode

#### **Technical Tasks**

- [ ] Create `src/components/avatar/InputModeToggle.vue`
- [ ] Update input area in `Chat.vue` to be mode-aware
- [ ] Add mode state to Pinia store
- [ ] Implement localStorage persistence
- [ ] Create toggle animation CSS
- [ ] Add mode-specific UI components

#### **Definition of Done**

- [ ] Toggle works smoothly between both modes
- [ ] Input area adapts correctly to selected mode
- [ ] Mode preference persists across sessions
- [ ] Visual feedback is clear and intuitive
- [ ] Integration with existing voice functionality works

---

## 🏗️ **Sprint Architecture**

### **New Components Created**

```
src/components/avatar/
├── AvatarPanel.vue           # Collapsible side panel container
├── ChatBubble.vue           # Individual message bubble
└── InputModeToggle.vue      # Voice/typing mode switcher
```

### **Modified Components**

```
src/views/Chat.vue            # Updated for bubble layout
src/components/chatbotStore.js # Enhanced with mode state
```

### **New State Management**

```javascript
// Added to chatbotStore.js or new avatarStore.js
const state = {
  avatarPanelVisible: false,
  inputMode: 'typing', // 'typing' | 'voice'
  // ... existing state
}
```

---

## 🎨 **Design Specifications**

### **Avatar Panel Specifications**

- **Desktop Width**: 320px
- **Mobile Behavior**: Full screen overlay
- **Animation**: 300ms ease slide from right
- **Background**: White with subtle shadow
- **Toggle Button**: Floating action button style

### **Chat Bubble Specifications**

- **User Messages**:
  - Background: #2196F3 (blue)
  - Text: White
  - Alignment: Right
  - Max width: 70% of container
- **AI Messages**:
  - Background: #F5F5F5 (light gray)
  - Text: #333 (dark gray)
  - Alignment: Left
  - Max width: 80% of container
- **Border Radius**: 18px with pointed corners
- **Spacing**: 8px between messages, 16px between groups

### **Input Toggle Specifications**

- **Toggle Width**: 120px
- **Toggle Height**: 40px
- **Animation**: 200ms ease slide
- **Colors**:
  - Active: #2196F3 (blue)
  - Inactive: #E0E0E0 (gray)

---

## 🧪 **Testing Plan**

### **Unit Tests**

- [ ] AvatarPanel show/hide functionality
- [ ] ChatBubble rendering with different message types
- [ ] InputModeToggle state changes
- [ ] localStorage persistence

### **Integration Tests**

- [ ] Panel doesn't interfere with existing chat
- [ ] Bubble layout works with existing message data
- [ ] Mode toggle integrates with voice functionality

### **User Acceptance Testing**

- [ ] Panel feels natural and non-intrusive
- [ ] Chat bubbles improve conversation readability
- [ ] Input mode switching is intuitive
- [ ] Mobile experience is smooth

### **Performance Tests**

- [ ] Panel animation runs at 60fps
- [ ] Bubble rendering doesn't lag with many messages
- [ ] No memory leaks with toggle usage

---

## 📊 **Sprint Metrics**

### **Velocity Tracking**

- **Total Story Points**: 26
- **Sprint Capacity**: 30 points (estimated)
- **Buffer**: 4 points for unexpected issues

### **Quality Gates**

- [ ] All acceptance criteria met
- [ ] Code coverage >80% for new components
- [ ] No console errors or warnings
- [ ] Performance: animations >60fps
- [ ] Accessibility: keyboard navigation works

### **Success Metrics**

- [ ] Panel toggle: <300ms animation time
- [ ] Chat bubbles: render <100ms per message
- [ ] Input toggle: state change <50ms
- [ ] Mobile responsive: works on screens >320px

---

## 🚀 **Sprint Demo Script**

### **Demo Flow** (5 minutes)

1. **Show current chat interface** - "This is where we started"
2. **Click avatar panel toggle** - "Watch the smooth slide-in animation"
3. **Display bubble messages** - "Notice the WeChat-style conversation flow"
4. **Toggle input modes** - "Users can switch between typing and voice"
5. **Test mobile responsive** - "Everything adapts to mobile screens"
6. **Show persistence** - "Settings are remembered across sessions"

### **Key Talking Points**

- Foundation is set for animated avatar
- Chat experience is more engaging and familiar
- Input flexibility improves user choice
- Mobile-first responsive design

---

## 🎯 **Sprint Retrospective Questions**

### **What Went Well?**

- Which component was easiest to implement?
- What design decisions felt most natural?
- Where did we exceed expectations?

### **What Could Improve?**

- Which integration points were more complex than expected?
- What would we design differently?
- Where did we encounter unexpected challenges?

### **Action Items for Next Sprint**

- Technical debt to address
- Architecture improvements needed
- Performance optimizations identified

---

*Sprint 1 ready for execution - building the foundation for an engaging animated avatar experience*
