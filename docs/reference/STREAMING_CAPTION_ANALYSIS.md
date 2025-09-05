# Streaming Caption Feature from audioTutor

**Reference Location**: `/reference/audioTutor/`  
**Repository**: https://github.com/tesolchina/audioTutor.git  
**Feature**: Real-time speech recognition with streaming captions

---

## 🎯 **Streaming Caption Overview**

The streaming caption feature provides **real-time visual feedback** of what the user is saying as they speak, before the final transcription is complete. This greatly improves user experience by showing immediate recognition of speech input.

### **Key Benefits:**
- ✅ **Immediate feedback** - Users see what's being recognized in real-time
- ✅ **Better user confidence** - Visual confirmation that speech is being captured
- ✅ **Error detection** - Users can spot recognition errors early
- ✅ **Professional UX** - Similar to YouTube live captions or Google Meet

---

## 🔧 **Technical Implementation**

### **Core Technology: Web Speech API**
**File**: `js/speech.js` (lines 13-45)

#### **Key Configuration:**
```javascript
this.recognition = new webkitSpeechRecognition();
this.recognition.continuous = true;
this.recognition.interimResults = true;  // ← CRITICAL for streaming
this.recognition.lang = UI.getSelectedLanguage();
```

#### **Result Handling:**
```javascript
handleResult: function(event) {
    let interimTranscript = '';
    
    // Process both final and interim results
    for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
            // Store final results permanently
            this.allRecognitionResults.push(event.results[i][0].transcript);
        } else {
            // Accumulate interim (temporary) results
            interimTranscript += event.results[i][0].transcript;
        }
    }
    
    // Display interim results in real-time
    if (interimTranscript !== '') {
        document.getElementById('interim-results').textContent = interimTranscript;
        document.getElementById('interim-results').style.display = 'block';
    }
}
```

---

## 🎨 **UI Implementation**

### **HTML Structure**
**File**: `index.html` (line 71)

```html
<!-- Interim results display -->
<div id="interim-results"></div>
```

### **CSS Styling**
**File**: `CSS/styles.css` (lines 270-284)

```css
#interim-results {
    position: absolute;
    bottom: 80px;           /* Above controls */
    left: 50%;
    transform: translateX(-50%);  /* Center horizontally */
    background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent */
    color: white;
    padding: 10px 15px;
    border-radius: 20px;    /* Rounded bubble */
    max-width: 80%;         /* Responsive width */
    display: none;          /* Hidden by default */
    z-index: 30;           /* Above other elements */
    text-align: center;
}
```

### **Visual Design:**
- **Floating bubble** positioned above controls
- **Semi-transparent background** for overlay effect
- **Rounded corners** for modern appearance
- **Responsive width** adapts to content
- **High z-index** ensures visibility over other elements

---

## 🔄 **Integration with ByteWise Frontend**

### **Current State Analysis**
**Our File**: `src/views/Avatar.vue`

Our current implementation:
```javascript
// We have basic speech recognition but no interim results
mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
};
```

### **Enhancement Plan**

#### **1. Add Web Speech API Integration**
**Target**: `src/views/Avatar.vue`

```javascript
// Add to data()
speechRecognition: null,
isListening: false,
interimTranscript: '',
finalTranscript: '',

// Add to methods
setupSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        this.speechRecognition = new webkitSpeechRecognition();
        this.speechRecognition.continuous = true;
        this.speechRecognition.interimResults = true;
        this.speechRecognition.lang = 'en-US'; // Make configurable
        
        this.speechRecognition.onresult = this.handleSpeechResult;
        this.speechRecognition.onerror = this.handleSpeechError;
    }
},

handleSpeechResult(event) {
    let interimTranscript = '';
    
    for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
            this.finalTranscript += transcript;
        } else {
            interimTranscript += transcript;
        }
    }
    
    // Update streaming caption
    this.interimTranscript = interimTranscript;
}
```

#### **2. Add Template Elements**
**Target**: `src/views/Avatar.vue` template

```vue
<template>
  <!-- Existing avatar content -->
  
  <!-- Add streaming caption overlay -->
  <div 
    v-if="interimTranscript && isListening" 
    class="streaming-caption"
  >
    {{ interimTranscript }}
  </div>
  
  <!-- Existing controls -->
</template>
```

#### **3. Add Styling**
**Target**: `src/views/Avatar.vue` or `src/style.css`

```css
.streaming-caption {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  max-width: 80%;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  z-index: 50;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
```

---

## 🚀 **Implementation Steps**

### **Phase 1: Basic Integration**
1. **Add Web Speech API** to existing voice recording
2. **Create interim results display** component
3. **Style streaming caption** overlay
4. **Test with existing voice flow**

### **Phase 2: Enhanced Features**
5. **Add language selection** for multilingual support
6. **Improve error handling** for speech recognition
7. **Add confidence indicators** for recognition quality
8. **Optimize for mobile** touch interactions

### **Phase 3: Advanced Features**
9. **Custom vocabulary** for educational terms
10. **Grammar correction** suggestions
11. **Pronunciation feedback** integration
12. **Accessibility improvements**

---

## 🎯 **User Experience Benefits**

### **Before (Current ByteWise):**
1. User clicks record
2. User speaks (no feedback)
3. User stops recording
4. Processing spinner appears
5. Final transcription shown

### **After (With Streaming Captions):**
1. User clicks record
2. User speaks → **Real-time caption appears**
3. User sees exactly what's being recognized
4. User can correct or continue based on interim feedback
5. Final processing with confirmed accuracy

---

## 🧪 **Testing Requirements**

### **Browser Compatibility**
- ✅ **Chrome**: Full Web Speech API support
- ⚠️ **Firefox**: Limited support, fallback needed
- ⚠️ **Safari**: iOS support varies
- ❌ **Other browsers**: Graceful degradation required

### **Language Support**
- ✅ **English (US)**: Primary target
- ✅ **Chinese (Simplified)**: Educational context
- ✅ **Cantonese**: Hong Kong market
- ✅ **Other languages**: Configurable support

### **Performance Testing**
- **Low latency**: < 100ms for interim results
- **Accuracy**: Compare interim vs final transcription
- **Memory usage**: Continuous recognition optimization
- **Battery impact**: Mobile device considerations

---

## 📋 **Implementation Checklist**

### **Core Functionality**
- [ ] Web Speech API integration in Avatar.vue
- [ ] Interim results handling and display
- [ ] CSS styling for caption overlay
- [ ] Integration with existing voice recording

### **User Experience**
- [ ] Smooth show/hide animations
- [ ] Responsive design for mobile
- [ ] Clear visual hierarchy with other UI elements
- [ ] Accessibility (screen reader compatibility)

### **Technical Robustness**
- [ ] Error handling for unsupported browsers
- [ ] Fallback for no microphone access
- [ ] Language selection integration
- [ ] Performance optimization

### **Testing & Deployment**
- [ ] Cross-browser testing
- [ ] Mobile device testing
- [ ] Testing environment deployment
- [ ] User acceptance testing

---

*Streaming caption feature analyzed and ready for implementation - will significantly improve user experience with real-time speech feedback*
