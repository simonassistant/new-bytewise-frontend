<template>
  <div v-if="show" class="bg-white w-full rounded-lg shadow-xl p-6 overflow-y-auto mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center border-b pb-3 mb-4">
      <h2 class="text-lg font-bold">📊 Learning Session Report</h2>
      <button class="text-gray-500 hover:text-gray-700 text-2xl" @click="$emit('close')">
        &times;
      </button>
    </div>

    <!-- Report Body -->
    <div class="text-sm space-y-4">
      <p><strong>Generated:</strong> {{ new Date().toLocaleString() }}</p>
      <p><strong>Total Messages:</strong> {{ chatHistory.length }}</p>
      <p><strong>Student Name:</strong> {{ userName || "No information given" }}</p>
      <p><strong>Student Email:</strong> {{ userEmail || "No information given" }}</p>

      <h3 class="text-lg font-semibold mt-4">📈 Your Contribution Analysis</h3>
      <div
        class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
        v-html="renderMarkdown(contributionAnalysis)"
      />
      <h3 class="text-lg font-semibold mt-4">📝 Complete Conversation</h3>
      <div class="bg-gray-50 p-4 rounded-lg max-h-[400px] overflow-y-auto">
        <div
          v-for="(msg, idx) in chatHistory"
          :key="idx"
          class="mb-3 p-3 rounded-md"
          :class="msg.role === 'user' ? 'bg-blue-50' : 'bg-green-50'"
        >
          <strong>{{ msg.role === "user" ? "👤 You" : "🤖 Assistant" }}:</strong>
          <div class="whitespace-pre-line mt-1">{{ msg.content }}</div>
          <div class="text-xs text-gray-500 mt-1">
            {{ new Date(msg.timestamp).toLocaleTimeString() }}
          </div>
        </div>
      </div>

      <hr class="my-4" />

      <div class="text-center text-gray-500 text-sm">
        <strong>Created by:</strong> Dr. Simon Wang, Innovation Officer<br />
        Language Centre, Hong Kong Baptist University<br />
        <a href="mailto:simonwang@hkbu.edu.hk" class="underline text-blue-600"
          >simonwang@hkbu.edu.hk</a
        >
      </div>
    </div>
    <!-- Footer -->
    <div class="mt-6 flex flex-wrap justify-end gap-1" v-if="!generatingAnalysis">
      <button
        class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:bg-gray-400 disabled:cursor-not-allowed"
        @click="sendReportByEmail"
        :disabled="emailSending"
      >
        <span v-if="emailSending">⏳ Sending...</span>
        <span v-else>Resend Report</span>
      </button>
      <button
        class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white"
        @click="downloadPDF"
      >
        Download PDF
      </button>
      <button
        class="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white"
        @click="downloadMarkdown"
      >
        Download Markdown
      </button>
      <button
        class="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-700 text-white"
        @click="copyReport"
      >
        Copy Text
      </button>
      <button
        class="px-4 py-2 rounded-lg bg-gray-600 hover:bg-gray-700 text-white"
        @click="$emit('close')"
      >
        Close
      </button>
    </div>

    <div v-else class="mt-6 text-center text-gray-500">⏳ Generating analysis, please wait...</div>

    <div class="text-sm text-gray-500 mt-4">Generated: {{ timestamp }}</div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { jsPDF } from "jspdf";
import MarkdownIt from "markdown-it";
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
const props = defineProps({
  show: Boolean,
  chatHistory: {
    type: Array,
    default: () => [],
  },
  reportGenerationInstructions: {
    type: String,
  },
  userEmail: {
    type: String,
  },
  userName: {
    type: String,
  },
  bccEmail: {
    type: Array,
  },
  ccEmail: {
    type: Array,
  },
  courseTitle: {
    type: String,
  },
});
function renderMarkdown(text) {
  return markdown.render(text || "");
}
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
        await sendReportByEmail();
      }
    }
  }
);

// ---------- Report Generation ----------
const reportHtml = computed(() => createReport(props.chatHistory));

function createReport(history) {
  if (!history.length) {
    return `<p>No conversation to report on.</p>`;
  }

  const now = new Date();

  let report = `
    <p><strong>Generated:</strong> ${now.toLocaleString()}</p>
    <p><strong>Total Messages:</strong> ${history.length}</p>
    <p><strong>Student Name:</strong> ${props.userName || "No information given"}</p>
     <p><strong>Student Email:</strong> ${props.userEmail || "No information given"}</p>
    <p><strong>Total Messages:</strong> ${history.length}</p>
    <h3>📈 Your Contribution Analysis</h3>
    <p>${contributionAnalysis.value}</p>

    <h3>📝 Complete Conversation</h3>
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; max-height: 400px; overflow-y: auto;">
  `;

  history.forEach((msg) => {
    report += `
      <div style="margin-bottom: 15px; padding: 10px; background: ${
        msg.role === "user" ? "#e3f2fd" : "#f1f8e9"
      }; border-radius: 6px;">
        <strong>${msg.role === "user" ? "👤 You" : "🤖 Assistant"}:</strong><br>
        ${msg.content.replace(/\n/g, "<br>")}
        <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
            ${msg.timestamp.toLocaleTimeString()}
        </div>
      </div>
    `;
  });

  report += "</div>";

  report += `
    <hr style="margin: 20px 0;">
    <div style="text-align: center; font-size: 0.9rem; color: #666;">
        <strong>Created by:</strong> Dr. Simon Wang, Innovation Officer<br>
        Language Centre, Hong Kong Baptist University<br>
        <a href="mailto:simonwang@hkbu.edu.hk">simonwang@hkbu.edu.hk</a>
    </div>
  `;

  return report;
}

async function analyzeContribution(userMessages, props) {
  generatingAnalysis.value = true;
  try {
    const chat_history = [
      {
        role: "user",
        content: `${props.reportGenerationInstructions}
        Below is the chat history. Please analyze the chat history according to the instructions above.
        Note that the chat history itself is not the instructions—the instructions provided earlier should guide your analysis.

        Chat history:
        ${JSON.stringify(userMessages)}`,
      },
    ];
    const res = await fetch(`${BASE_URL}/chatbot/chat_openrouter`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history,
        api_key: "", // fill in if required
        model_name: "gpt-4.1-mini",
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
  doc.text(`Student name: ${props.userName || "No information given"}`, 20, yPos);
  yPos += 7;
  doc.text(`Student email: ${props.userEmail || "No information given"}`, 20, yPos);
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
**Student Name:** ${props.userName || "No information given"}
**Student Email:** ${props.userEmail || "No information given"}
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

function copyReport() {
  const el = document.createElement("textarea");
  el.value = reportHtml.value.replace(/<[^>]+>/g, ""); // strip HTML
  document.body.appendChild(el);
  el.select();
  try {
    document.execCommand("copy");
    alert("Report copied to clipboard!");
  } catch {
    alert("Failed to copy report");
  }
  document.body.removeChild(el);
}

const emailSending = ref(false);
const emailSent = ref(false);
import { BASE_URL } from "../base_url";

async function sendReportByEmail() {
  const history = props.chatHistory;
  if (!history.length) {
    alert("No conversation to export");
    return;
  }
  console.log(props.userEmail);
  // Validate student email address
  if (!isValidEmail(props.userEmail)) {
    alert("Please enter a valid email address in the user information sidebar.");
    return;
  }

  emailSending.value = true;

  await fetch(`${BASE_URL}/sendEmail/send-email`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_email: props.userEmail,
      student_name: props.userName || "No information given",
      bccEmail: props.bccEmail,
      ccEmail: props.ccEmail,
      report_history: history,
      contributionAnalysis: contributionAnalysis.value,
      course_title: props.courseTitle,
    }),
  })
    .then((response) => {
      if (response.ok) {
        emailSent.value = true;
        alert(
          "Report sent successfully! (It may take a few minutes to arrive, please check your spam folder if you can not receive the email)"
        );
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
