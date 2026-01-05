<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white w-full max-w-3xl rounded-lg shadow-xl p-6 overflow-y-auto max-h-[90vh]">
      <!-- Header -->
      <div class="flex justify-between items-center border-b pb-3 mb-4">
        <h2 class="text-lg font-bold">📊 Learning Session Report</h2>
        <button class="text-gray-500 hover:text-gray-700 text-2xl" @click="$emit('close')">
          &times;
        </button>
      </div>

      <p><strong>Total Messages:</strong> {{ props.chatHistory.length }}</p>
      <h3>📈 Your Contribution Analysis</h3>
      <div
        class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
        v-html="renderMarkdown(contributionAnalysis)"
      />
      <h3>📝 Complete Conversation</h3>
      <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div
          v-for="(msg, i) in chatHistory"
          :key="i"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-lg md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
            :class="msgClasses(msg, i)"
          >
            <div class="font-semibold text-xs mb-1">
              {{ msgSenderLabel(msg.role) }}
            </div>

            <div
              class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
              v-html="renderMarkdown(msg.content)"
            />
          </div>
        </div>
      </div>
      <!-- User Input Section -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg border">
        <h3 class="text-md font-semibold mb-3 text-gray-700">📧 Email Settings</h3>
        <div class="space-y-3">
          <div>
            <label for="studentEmail" class="block text-sm font-medium text-gray-700 mb-1">
              Your Email Address:
            </label>
            <input
              id="studentEmail"
              v-model="student_email"
              type="email"
              placeholder="Enter your email address"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
        </div>
      </div>
      <!-- Footer -->
      <div class="mt-6 flex flex-wrap justify-end gap-1" v-if="!generatingAnalysis">
        <button
          class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:bg-gray-400 disabled:cursor-not-allowed"
          @click="sendReportByEmail"
          :disabled="emailSending || !isValidEmail(student_email)"
        >
          <span v-if="emailSending">⏳ Sending...</span>
          <span v-else>📧 Send Report</span>
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white"
          @click="downloadPDF"
        >
          📥 Download PDF
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white"
          @click="downloadMarkdown"
        >
          📝 Download Markdown
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-700 text-white"
          @click="copyReport"
        >
          📋 Copy Text
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-gray-600 hover:bg-gray-700 text-white"
          @click="$emit('close')"
        >
          Close
        </button>
      </div>
      <div v-else class="mt-6 text-center text-gray-500">
        ⏳ Generating analysis, please wait...
      </div>
      <div class="text-sm text-gray-500 mt-4">Generated: {{ timestamp }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { jsPDF } from "jspdf";
import MarkdownIt from "markdown-it";
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
const emit = defineEmits(["submit"]);
const props = defineProps({
  show: Boolean,
  chatHistory: {
    type: Array,
    default: () => [],
  },
  reportGenerationInstructions: {
    type: String,
  },
  bccEmail: {
    type: Array,
  },
  hiddenReport: {
    type: String,
  },
  ccEmail: {
    type: Array,
  },
});

// timestamp
const timestamp = ref("");
const contributionAnalysis = ref("[Analyzing contribution...]");
const generatingAnalysis = ref(true);
// update timestamp whenever modal is opened
watch(
  () => props.show,
  async (val) => {
    if (val) {
      timestamp.value = new Date().toLocaleString();

      // only fetch once when shown
      if (props.chatHistory.length) {
        contributionAnalysis.value = "[Analyzing contribution...]";
        contributionAnalysis.value = await analyzeContribution(props.chatHistory, props);
      }
    }
  }
);
function renderMarkdown(text) {
  return markdown.render(text || "");
}
function msgSenderLabel(role) {
  return role === "user" ? "You" : "AI Assistant";
}

function msgClasses(msg) {
  return msg.role === "user"
    ? "bg-indigo-600 text-white rounded-br-none"
    : "bg-gray-100 text-gray-800 rounded-bl-none";
}
// ---------- Report Generation ----------

async function analyzeContribution(userMessages, props) {
  generatingAnalysis.value = true;
  try {
    const chat_history = [
      {
        role: "user",
        content: `${props.reportGenerationInstructions} here are the chat history ${JSON.stringify(
          userMessages
        )}`,
      },
    ];
    const res = await fetch(`${BASE_URL}/chatbot/chat_openrouter`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history,
        api_key: "", // fill in if required
        model_name: "gpt-4.1-mini",
        temperature: 0.0,
      }),
    });

    const data = await res.json();
    return data?.choices?.[0]?.message?.content || data?.error || "[No response]";
  } catch (err) {
    console.error("Error analyzing contribution:", err);
    return "[Request failed]";
  } finally {
    generatingAnalysis.value = false;
  }
}

// ---------- Actions ----------
function downloadPDF() {
  const history = props.chatHistory;
  if (!history.length) {
    alert("No conversation to export");
    return;
  }

  const doc = new jsPDF();
  let yPos = 20;

  // Title
  doc.setFontSize(18);
  doc.text("HKBU Learning Session Report", 20, yPos);
  yPos += 15;

  // Metadata
  const now = new Date();

  doc.setFontSize(12);
  doc.text(`Generated: ${now.toLocaleString()}`, 20, yPos);
  yPos += 7;
  doc.text(`Total Messages: ${history.length}`, 20, yPos);
  yPos += 15;

  // ✅ Contribution Analysis (keep this)
  doc.setFontSize(14);
  doc.text("Your Contribution Analysis", 20, yPos);
  yPos += 7;
  doc.setFontSize(11);
  const analysisLines = doc.splitTextToSize(contributionAnalysis.value, 170);
  analysisLines.forEach((line) => {
    if (yPos > 270) {
      doc.addPage();
      yPos = 20;
    }
    doc.text(line, 20, yPos);
    yPos += 6;
  });
  yPos += 10;

  // Conversation
  doc.setFontSize(14);
  doc.text("Complete Conversation", 20, yPos);
  yPos += 10;

  doc.setFontSize(11);
  history.forEach((msg) => {
    if (yPos > 270) {
      doc.addPage();
      yPos = 20;
    }

    const role = msg.role === "user" ? "You:" : "Assistant:";
    doc.setFont(undefined, "bold");
    doc.text(role, 20, yPos);
    doc.setFont(undefined, "normal");
    yPos += 6;

    const lines = doc.splitTextToSize(msg.content, 170);
    lines.forEach((line) => {
      if (yPos > 270) {
        doc.addPage();
        yPos = 20;
      }
      doc.text(line, 20, yPos);
      yPos += 6;
    });

    doc.setFontSize(9);
    doc.text(msg.timestamp.toLocaleTimeString(), 20, yPos);
    doc.setFontSize(11);
    yPos += 10;
  });

  // Footer
  if (yPos > 250) {
    doc.addPage();
    yPos = 20;
  }
  yPos += 10;
  doc.setFontSize(10);
  doc.text("Created by: Dr. Simon Wang, Innovation Officer", 20, yPos);
  yPos += 5;
  doc.text("Language Centre, Hong Kong Baptist University", 20, yPos);
  yPos += 5;
  doc.text("simonwang@hkbu.edu.hk", 20, yPos);

  doc.save(`HKBU_Learning_Report_${new Date().toISOString().split("T")[0]}.pdf`);
}

function downloadMarkdown() {
  const report = createMarkdownReport(props.chatHistory);
  const blob = new Blob([report], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `HKBU_Learning_Report_${new Date().toISOString().split("T")[0]}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function createMarkdownReport(history) {
  const now = new Date();
  let markdown = `# 📊 HKBU Learning Session Report

**Generated:** ${now.toLocaleString()}
**Total Messages:** ${history.length}

## 📈 Your Contribution Analysis

${contributionAnalysis.value}

## 📝 Complete Conversation

`;

  history.forEach((msg) => {
    const role = msg.role === "user" ? "👤 **You**" : "🤖 **Assistant**";
    markdown += `### ${role} (${msg.timestamp.toLocaleTimeString()})\n\n${msg.content}\n\n`;
  });

  markdown += `---
*Created by: Dr. Simon Wang, Innovation Officer*
*Language Centre, Hong Kong Baptist University*
*simonwang@hkbu.edu.hk*`;

  return markdown;
}

async function copyReport() {
  try {
    const report = createMarkdownReport(props.chatHistory);
    await navigator.clipboard.writeText(report);
    alert("✅ Full markdown report copied to clipboard!");
  } catch (error) {
    console.error("Failed to copy report:", error);
    alert("❌ Failed to copy report.");
  }
}

const student_email = ref("");
const emailSending = ref(false);
const emailSent = ref(false);
import { BASE_URL } from "@/components/base_url";

function sendReportByEmail() {
  const history = props.chatHistory;
  if (!history.length) {
    alert("No conversation to export");
    return;
  }

  // Validate student email address
  if (!isValidEmail(student_email.value)) {
    alert("Please enter a valid email address");
    return;
  }

  emailSending.value = true;

  fetch(`${BASE_URL}/sendEmail/send-email`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_email: student_email.value,
      bccEmail: props.bccEmail,
      ccEmail: props.ccEmail,
      report_md: createMarkdownReport(history),
      report_history: history,
      hiddenReport: props.hiddenReport,
      contributionAnalysis: contributionAnalysis.value,
    }),
  })
    .then((response) => {
      if (response.ok) {
        emailSent.value = true;
        alert(
          "Report sent successfully! (It may take a few minutes to arrive, please check your spam folder if you can not receive the email)"
        );
        emit("submit");
      } else {
        throw new Error("Failed to send email");
      }
    })
    .catch((error) => {
      alert(`Error: ${error.message}`);
    })
    .finally(() => {
      emailSending.value = false;
    });
}

// Email validation function
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
</script>
