# Email Integration Workflow Notes

## Overview for Email Feature Implementation

This document provides guidance on implementing email functionality in our ByteWise chatbot system, allowing users to send their session reports via email to both themselves and their teachers.

## Current Report Generation Flow

1. After a chat session, users click the "Finish & View Report" button (green checkmark).
2. This triggers the `showReport = true` state in `Chat.vue`, which displays the `ReportModal` component.
3. The `ReportModal` receives the chat history and generates a formatted report.

## Email Feature Implementation Requirements

### User Flow
1. User completes a chatbot session
2. User views the report summary
3. User enters their email address
4. User confirms sending to themselves and the teacher
5. System sends emails and shows confirmation

### Key Files to Modify

#### 1. `src/components/ReportModal.vue`
This is the **primary file** you'll need to modify. It currently displays the session report and needs to be enhanced with email functionality.

```vue
<!-- Current structure (simplified) -->
<template>
  <div v-if="show" class="report-modal">
    <div class="report-content">
      <h2>Session Report</h2>
      <!-- Report summary section -->
      <div class="report-summary">...</div>
      
      <!-- Report conversation section -->
      <div class="report-conversation">...</div>
      
      <!-- Buttons -->
      <div class="button-group">
        <button @click="$emit('close')">Close</button>
        <!-- Add email form and button here -->
      </div>
    </div>
  </div>
</template>
```

#### Proposed Changes to ReportModal.vue

Add this form section before the button group:

```vue
<!-- Email form to add -->
<div class="email-section mt-6 border-t border-gray-200 pt-4">
  <h3 class="text-lg font-semibold mb-2">Send Report via Email</h3>
  
  <!-- Step 1: Email collection form (initially visible) -->
  <div v-if="emailStep === 'collection'">
    <div class="mb-3">
      <label class="block text-sm font-medium mb-1">Your Email Address</label>
      <input 
        type="email" 
        v-model="userEmail" 
        placeholder="Enter your email address" 
        class="w-full p-2 border border-gray-300 rounded"
      />
    </div>
    
    <div class="flex items-center mb-4">
      <input 
        type="checkbox" 
        id="saveEmail" 
        v-model="saveEmailPreference"
        class="mr-2"
      />
      <label for="saveEmail" class="text-sm text-gray-600">Remember my email for future sessions</label>
    </div>
    
    <button 
      @click="proceedToConfirmation" 
      :disabled="!isValidEmail" 
      class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:bg-gray-400"
    >
      Continue
    </button>
  </div>
  
  <!-- Step 2: Confirmation screen -->
  <div v-if="emailStep === 'confirmation'">
    <p class="mb-4">This report will be sent to:</p>
    <ul class="list-disc ml-6 mb-4">
      <li>Your email: {{ userEmail }}</li>
      <li v-if="teacherEmail">Teacher's email: {{ teacherEmail }}</li>
    </ul>
    
    <div class="flex gap-3">
      <button 
        @click="sendReport" 
        :disabled="emailSending" 
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
      >
        {{ emailSending ? 'Sending...' : 'Confirm & Send' }}
      </button>
      <button 
        @click="emailStep = 'collection'" 
        class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
      >
        Back
      </button>
    </div>
  </div>
  
  <!-- Step 3: Success message -->
  <div v-if="emailStep === 'success'" class="text-center py-3">
    <div class="text-green-600 text-xl mb-2">✓</div>
    <p>Report successfully sent!</p>
  </div>
  
  <!-- Error message -->
  <div v-if="emailError" class="mt-3 p-3 bg-red-50 border border-red-200 text-red-700 rounded">
    {{ emailError }}
  </div>
</div>
```

Add these script sections:

```javascript
// Add to the existing script section
import { useChatbotStore } from "../components/chatbotStore";

// Add to the data section
const chatbotStore = useChatbotStore();
const userEmail = ref('');
const teacherEmail = ref(''); // This could be fetched from the bot config or API
const saveEmailPreference = ref(false);
const emailStep = ref('collection'); // collection, confirmation, success
const emailSending = ref(false);
const emailError = ref(null);

// Add these computed properties
const isValidEmail = computed(() => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userEmail.value);
});

// Add these methods
function proceedToConfirmation() {
  if (!isValidEmail.value) return;
  
  // Get teacher's email - you might need to modify this logic
  // depending on how teacher emails are stored
  teacherEmail.value = selectedBot.value.teacherEmail || '';
  
  emailStep.value = 'confirmation';
}

async function sendReport() {
  if (emailSending.value) return;
  
  emailSending.value = true;
  emailError.value = null;
  
  try {
    // This is where your colleague's email sending module will be integrated
    const response = await fetch(
      "https://smartlessons-production.up.railway.app/api/email",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userEmail: userEmail.value,
          teacherEmail: teacherEmail.value,
          subject: `${selectedBot.value.name} Chat Report`,
          reportContent: generateEmailHTML(),
          apiKey: chatbotStore.apiKey,
        }),
      }
    );
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send email');
    }
    
    // Save user's email preference if selected
    if (saveEmailPreference.value) {
      chatbotStore.setUserEmail(userEmail.value);
    }
    
    // Show success message
    emailStep.value = 'success';
  } catch (error) {
    console.error('Email sending error:', error);
    emailError.value = error.message || 'Something went wrong. Please try again.';
  } finally {
    emailSending.value = false;
  }
}

function generateEmailHTML() {
  // You can reuse your existing report generation logic
  // or create a specific version for email
  return `
    <h1>${selectedBot.value.name} Session Report</h1>
    <p><strong>Date:</strong> ${new Date().toLocaleString()}</p>
    <p><strong>Duration:</strong> ${duration} minutes</p>
    <p><strong>Messages:</strong> ${props.chatHistory.length}</p>
    
    <h2>Conversation</h2>
    ${props.chatHistory.map(msg => `
      <div style="margin-bottom: 15px;">
        <strong>${msg.role === 'user' ? 'You' : 'Assistant'}:</strong>
        <p>${msg.content}</p>
        <small>${new Date(msg.timestamp).toLocaleString()}</small>
      </div>
    `).join('')}
  `;
}

// Add to onMounted or created hook
onMounted(() => {
  // Try to load saved email if available
  const savedEmail = chatbotStore.userPreferences?.email;
  if (savedEmail) {
    userEmail.value = savedEmail;
    saveEmailPreference.value = true;
  }
});
```

#### 2. `src/components/chatbotStore.js`

You'll need to enhance the store to save user email preferences. Add these properties and methods:

```javascript
// Add to the state object
state: () => ({
  // existing state properties...
  
  userPreferences: {
    email: null,
  }
}),

// Add these actions
actions: {
  // existing actions...
  
  setUserEmail(email) {
    this.userPreferences.email = email;
    localStorage.setItem('user_email_pref', email);
  },
  
  loadUserPreferences() {
    const email = localStorage.getItem('user_email_pref');
    if (email) {
      this.userPreferences.email = email;
    }
  }
}
```

#### 3. `src/botConfig/*.json` files

These contain bot configurations. You may want to add a `teacherEmail` field to these configuration files to specify the teacher's email address for each bot type:

```json
{
  "name": "IELTS Writing Tutor",
  "systemPrompt": "You are an IELTS Writing Tutor...",
  "welcomePrompt": "Hello! I am your IELTS...",
  "model": "gpt-4.1",
  "teacherEmail": "writing.teacher@example.com"
}
```

## Backend API Requirements

Your colleague will need to implement a backend endpoint to handle the email sending. The expected endpoint is:

```
POST https://smartlessons-production.up.railway.app/api/email
```

Expected request body:
```json
{
  "userEmail": "student@example.com",
  "teacherEmail": "teacher@example.com",
  "subject": "Chat Report: IELTS Writing Tutor",
  "reportContent": "<html>...</html>",
  "apiKey": "user_api_key_here"
}
```

Expected responses:
- `200 OK` - Email sent successfully
- `400 Bad Request` - Invalid email format or missing required fields
- `401 Unauthorized` - Invalid API key
- `500 Internal Server Error` - Server-side error

## Integration Notes

1. **Email Validation**: Implement client-side validation to ensure users enter valid email addresses.

2. **Storage Consideration**: If storing user emails, ensure compliance with privacy regulations.

3. **Error Handling**: Provide clear feedback to users if email sending fails.

4. **Teacher Emails**: Consider whether teacher emails should be hardcoded in bot configurations or managed through a separate admin interface.

5. **HTML Email Template**: Format the email content for readability, possibly using a more sophisticated template than the simple example provided.

6. **Accessibility**: Ensure the email form is accessible to all users, including those using screen readers.

## Testing Workflow

1. Complete a chat session
2. Click "Finish & View Report"
3. Enter email details
4. Confirm sending
5. Verify emails are received by both user and teacher
6. Check that the email format is correct and readable

## Additional Resources

- [Vue.js Form Validation](https://vuejs.org/guide/essentials/forms.html)
- [Email HTML Templates Best Practices](https://www.litmus.com/blog/email-design-best-practices/)
- [Client-side Email Validation Regex](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/email)

## Contact for Questions

If you have any questions about the frontend implementation or need clarification on how the current report generation works, please contact our team.

---

*Note: This document outlines the proposed implementation. The actual code may need adjustments based on your specific email sending module's requirements and capabilities.*
