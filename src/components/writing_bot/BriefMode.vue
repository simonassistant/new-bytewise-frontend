<template>
  <div class="space-y-8">
    <!-- Header Section -->
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">EditForge: AI-Powered Writing Assistant</h1>
      <p class="text-gray-600">Develop essential AI collaboration skills through structured writing revision tasks</p>
    </div>

    <!-- Overview Section - Always Visible -->
    <div class="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <div class="border-l-4 border-indigo-500 pl-4">
        <h2 class="text-xl font-bold text-indigo-600 mb-4">System Overview</h2>
        <div class="space-y-4">
          <p class="text-gray-700 leading-relaxed">
            EditForge is an AI-powered writing assistant designed to help students develop essential AI collaboration skills through structured writing revision tasks. The system consists of three main modes:
          </p>
          
          <div class="grid md:grid-cols-3 gap-4">
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="font-semibold text-blue-800 mb-2">🎯 Training Mode</h3>
              <p class="text-sm text-blue-700">Learn how to effectively collaborate with AI for writing improvement through guided conversations.</p>
            </div>
            <div class="bg-purple-50 p-4 rounded-lg">
              <h3 class="font-semibold text-purple-800 mb-2">📝 Assessment Mode</h3>
              <p class="text-sm text-purple-700">Demonstrate learned AI collaboration skills independently through self-directed conversations.</p>
            </div>
            <div class="bg-green-50 p-4 rounded-lg">
              <h3 class="font-semibold text-green-800 mb-2">📋 Briefing Mode</h3>
              <p class="text-sm text-green-700">Understand tasks, rubrics, and expectations through detailed guidelines and assessment criteria.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toggle Sections -->
    <div class="space-y-4">
      <!-- For Teachers Toggle -->
      <div class="bg-white rounded-lg shadow-lg">
        <button
          @click="toggleSection('teachers')"
          class="w-full p-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors"
        >
          <h2 class="text-lg font-semibold text-gray-800">For Teachers</h2>
          <span class="text-gray-500">{{ sections.teachers ? '−' : '+' }}</span>
        </button>
        <div v-if="sections.teachers" class="px-4 pb-4 border-t">
          <div class="pt-4 space-y-4">
            <div class="prose prose-sm max-w-none">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">System Setup and Management</h3>
              <div class="bg-yellow-50 p-4 rounded-lg mb-4">
                <h4 class="font-semibold text-yellow-800 mb-2">API Configuration</h4>
                <ul class="text-sm text-yellow-700 space-y-1">
                  <li><strong>Platform:</strong> HKBU Generative AI Platform</li>
                  <li><strong>Access:</strong> <a href="https://genai.hkbu.edu.hk/settings/api-docs" target="_blank" class="text-blue-600 hover:underline">https://genai.hkbu.edu.hk/settings/api-docs</a></li>
                  <li><strong>Key Management:</strong> Generate and securely store API keys</li>
                  <li><strong>Student Access:</strong> Guide students through API key generation process</li>
                </ul>
              </div>

              <h3 class="text-lg font-semibold text-gray-800 mb-3">Assessment Implementation</h3>
              <div class="grid md:grid-cols-2 gap-4 mb-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-blue-800 mb-2">Training Mode (Task 1 - 10%)</h4>
                  <p class="text-sm text-blue-700 mb-2">Students learn AI collaboration skills with guidance</p>
                  <ul class="text-xs text-blue-600 space-y-1">
                    <li>• Monitor student engagement</li>
                    <li>• Provide feedback on AI interaction quality</li>
                    <li>• Guide students in providing contextual information</li>
                  </ul>
                </div>
                <div class="bg-purple-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-purple-800 mb-2">Assessment Mode (Task 2 - 10%)</h4>
                  <p class="text-sm text-purple-700 mb-2">Students demonstrate independent AI collaboration skills</p>
                  <ul class="text-xs text-purple-600 space-y-1">
                    <li>• Quality of AI conversations</li>
                    <li>• Critical evaluation of AI suggestions</li>
                    <li>• Strategic revision decisions</li>
                  </ul>
                </div>
              </div>

              <h3 class="text-lg font-semibold text-gray-800 mb-3">Best Practices</h3>
              <div class="bg-gray-50 p-4 rounded-lg">
                <div class="grid md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <h4 class="font-semibold text-gray-800 mb-2">Pre-Assessment</h4>
                    <ul class="text-gray-600 space-y-1">
                      <li>• Demo sessions</li>
                      <li>• Practice runs</li>
                      <li>• Clear expectations</li>
                    </ul>
                  </div>
                  <div>
                    <h4 class="font-semibold text-gray-800 mb-2">During Assessment</h4>
                    <ul class="text-gray-600 space-y-1">
                      <li>• Monitor progress</li>
                      <li>• Provide support</li>
                      <li>• Encourage engagement</li>
                    </ul>
                  </div>
                  <div>
                    <h4 class="font-semibold text-gray-800 mb-2">Post-Assessment</h4>
                    <ul class="text-gray-600 space-y-1">
                      <li>• Detailed feedback</li>
                      <li>• Encourage reflection</li>
                      <li>• Identify improvements</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- For Students Toggle -->
      <div class="bg-white rounded-lg shadow-lg">
        <button
          @click="toggleSection('students')"
          class="w-full p-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors"
        >
          <h2 class="text-lg font-semibold text-gray-800">For Students</h2>
          <span class="text-gray-500">{{ sections.students ? '−' : '+' }}</span>
        </button>
        <div v-if="sections.students" class="px-4 pb-4 border-t">
          <div class="pt-4 space-y-4">
            <div class="prose prose-sm max-w-none">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">What You'll Learn</h3>
              <div class="grid md:grid-cols-2 gap-4 mb-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-blue-800 mb-2">🤖 AI Collaboration Skills</h4>
                  <ul class="text-sm text-blue-700 space-y-1">
                    <li>• Effective communication with AI assistants</li>
                    <li>• Providing context and background information</li>
                    <li>• Critically evaluating AI suggestions</li>
                    <li>• Making strategic revision decisions</li>
                  </ul>
                </div>
                <div class="bg-green-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-green-800 mb-2">✍️ Writing Improvement Skills</h4>
                  <ul class="text-sm text-green-700 space-y-1">
                    <li>• Content organization and development</li>
                    <li>• Grammar and vocabulary enhancement</li>
                    <li>• Structural and logical progression</li>
                    <li>• Critical thinking about your writing</li>
                  </ul>
                </div>
              </div>

              <h3 class="text-lg font-semibold text-gray-800 mb-3">Your Assessment Journey</h3>
              <div class="space-y-4 mb-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-blue-800 mb-2">Step 1: Training Mode (Task 1 - 10%)</h4>
                  <p class="text-sm text-blue-700 mb-2">Guided conversations with AI to revise a teacher-provided essay</p>
                  <div class="text-xs text-blue-600">
                    <strong>Your Goals:</strong> Engage meaningfully, provide context, ask thoughtful questions, make informed decisions
                  </div>
                </div>
                <div class="bg-purple-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-purple-800 mb-2">Step 2: Assessment Mode (Task 2 - 10%)</h4>
                  <p class="text-sm text-purple-700 mb-2">Independent conversations with AI to revise your own essay</p>
                  <div class="text-xs text-purple-600">
                    <strong>Your Goals:</strong> Conduct deep conversations, critically evaluate suggestions, make strategic decisions
                  </div>
                </div>
              </div>

              <h3 class="text-lg font-semibold text-gray-800 mb-3">How to Succeed</h3>
              <div class="grid md:grid-cols-2 gap-4">
                <div class="space-y-3">
                  <div class="bg-yellow-50 p-3 rounded-lg">
                    <h4 class="font-semibold text-yellow-800 mb-1">🎯 Provide Context to AI</h4>
                    <p class="text-xs text-yellow-700">Tell AI about your course context, writing goals, challenges, and focus areas.</p>
                  </div>
                  <div class="bg-red-50 p-3 rounded-lg">
                    <h4 class="font-semibold text-red-800 mb-1">🤔 Ask Critical Questions</h4>
                    <p class="text-xs text-red-700">Don't accept suggestions blindly. Ask "Why?" and "How?" questions.</p>
                  </div>
                </div>
                <div class="space-y-3">
                  <div class="bg-green-50 p-3 rounded-lg">
                    <h4 class="font-semibold text-green-800 mb-1">📋 Plan Your Strategy</h4>
                    <p class="text-xs text-green-700">Start with content/organization, then move to grammar/vocabulary.</p>
                  </div>
                  <div class="bg-blue-50 p-3 rounded-lg">
                    <h4 class="font-semibold text-blue-800 mb-1">⏰ Manage Your Time</h4>
                    <p class="text-xs text-blue-700">Allocate 1-2 hours per task, aim for 10-50 conversation rounds.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Context and Goals Toggle -->
      <div class="bg-white rounded-lg shadow-lg">
        <button
          @click="toggleSection('context')"
          class="w-full p-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors"
        >
          <h2 class="text-lg font-semibold text-gray-800">Context and Goals</h2>
          <span class="text-gray-500">{{ sections.context ? '−' : '+' }}</span>
        </button>
        <div v-if="sections.context" class="px-4 pb-4 border-t">
          <div class="pt-4 space-y-4">
            <div class="prose prose-sm max-w-none">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">Educational Context</h3>
              <div class="bg-indigo-50 p-4 rounded-lg mb-4">
                <p class="text-sm text-indigo-700">
                  This system is designed for first-year students in remedial English courses. The goal is to develop essential AI collaboration skills while improving writing abilities through structured, interactive revision processes.
                </p>
              </div>

              <h3 class="text-lg font-semibold text-gray-800 mb-3">Learning Objectives</h3>
              <div class="grid md:grid-cols-3 gap-4 mb-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-blue-800 mb-2">AI Collaboration Skills</h4>
                  <ul class="text-sm text-blue-700 space-y-1">
                    <li>• Effective communication with AI</li>
                    <li>• Context provision and goal setting</li>
                    <li>• Critical evaluation of AI suggestions</li>
                  </ul>
                </div>
                <div class="bg-green-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-green-800 mb-2">Writing Revision Skills</h4>
                  <ul class="text-sm text-green-700 space-y-1">
                    <li>• Content organization and development</li>
                    <li>• Grammar and vocabulary improvement</li>
                    <li>• Structural and logical progression</li>
                  </ul>
                </div>
                <div class="bg-purple-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-purple-800 mb-2">Critical Thinking Skills</h4>
                  <ul class="text-sm text-purple-700 space-y-1">
                    <li>• Decision-making in revision processes</li>
                    <li>• Evaluation of AI feedback quality</li>
                    <li>• Strategic planning for improvement</li>
                  </ul>
                </div>
              </div>

              <h3 class="text-lg font-semibold text-gray-800 mb-3">Assessment Structure</h3>
              <div class="space-y-3">
                <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                  <div>
                    <h4 class="font-semibold text-gray-800">Task 1: Guided Chatbot Revision (10%)</h4>
                    <p class="text-sm text-gray-600">Training Mode - Learn AI collaboration with guidance</p>
                  </div>
                </div>
                <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div class="w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                  <div>
                    <h4 class="font-semibold text-gray-800">Task 2: Independent AI-Assisted Review (10%)</h4>
                    <p class="text-sm text-gray-600">Assessment Mode - Apply skills independently</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Assessment Tasks Section -->
    <div class="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <div class="border-l-4 border-blue-500 pl-4">
        <h2 class="text-xl font-bold text-blue-600 mb-2">
          Task 1: Point-of-View Essay with Guided Chatbot Revision (10%)
        </h2>
        <p class="text-gray-700 leading-relaxed">
          In this task, students will engage in a conversation with a chatbot to revise a
          teacher-provided draft essay. The chatbot will provide appropriate prompts to guide the
          discussion, helping students identify areas for improvement and refine the draft into a
          stronger point-of-view essay. The goal is to enhance the essay's content, organization,
          vocabulary, and grammar through interactive feedback.
        </p>
      </div>

      <div>
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Rubric for Point-of-View Essay</h3>
        <div class="overflow-x-auto">
          <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden shadow-sm">
            <thead>
              <tr class="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Criteria</th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  1 (Limited)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  2 (Basic)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  3 (Developing)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  4 (Proficient)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  5 (Excellent)
                </th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr class="hover:bg-blue-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">
                  A. Content and Ideas
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Ideas are irrelevant or minimally related to the topic; lacks awareness of the
                  issue; no clear viewpoint
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Ideas are somewhat related but vague; minimal awareness of the issue; viewpoint
                  unclear
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Ideas are relevant but basic; some awareness of the issue; viewpoint present but
                  weakly developed
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Ideas are relevant and solid; good awareness of the issue; clear viewpoint with
                  some depth
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Ideas are insightful and highly relevant; strong awareness of the issue;
                  well-developed, compelling viewpoint
                </td>
              </tr>
              <tr class="hover:bg-blue-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">
                  B. Organisation and Logical Progression
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  No clear structure; ideas are disjointed with no development or progression
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Basic structure with unclear paragraphing; ideas are listed with little
                  development
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Clear structure with some paragraphing; ideas are developed but lack depth or
                  logical flow
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Well-organised with clear paragraphs; ideas are developed logically with good flow
                  and support
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Highly organised with effective paragraphing; ideas are thoroughly developed with
                  seamless, logical progression
                </td>
              </tr>
              <tr class="hover:bg-blue-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">
                  C. Vocabulary
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Vocabulary is limited, repetitive, or inaccurate; lacks topic-specific terms
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Basic vocabulary with some repetition; minimal use of topic-specific terms
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Adequate vocabulary with some variety; includes some topic-specific terms but with
                  occasional errors
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Varied and precise vocabulary; effective use of topic-specific terms; minor errors
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Rich, precise vocabulary; masterful use of topic-specific terms; almost error-free
                  and sophisticated
                </td>
              </tr>
              <tr class="hover:bg-blue-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-blue-100">
                  D. Grammar and Sentence Structure
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Frequent grammatical and spelling errors; sentences are incomplete or confusing
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Several grammatical and spelling errors; sentences are simple and often flawed
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Some grammatical and spelling errors; sentences are mostly correct but lack
                  variety
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Minor grammatical and spelling errors; sentences are varied and mostly accurate
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Virtually error-free grammar and spelling; sentences are complex, varied, and
                  accurately constructed
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <div class="border-l-4 border-purple-500 pl-4">
        <h2 class="text-xl font-bold text-purple-600 mb-2">
          Task 2: AI-Assisted Review of Student Draft (10%)
        </h2>
        <p class="text-gray-700 leading-relaxed">
          In this task, students will independently engage in a conversation with a chatbot to
          revise their own draft essay, without any prompts provided. The focus is on learning how
          to critically assess and refine their work through interaction with the chatbot, improving
          the essay's overall quality based on the feedback received.
        </p>
      </div>

      <div>
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Rubric for AI-Assisted Review</h3>
        <div class="overflow-x-auto">
          <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden shadow-sm">
            <thead>
              <tr class="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
                <th class="border border-gray-300 px-4 py-3 text-left font-semibold">Criteria</th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  1 (Limited)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  2 (Basic)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  3 (Developing)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  4 (Proficient)
                </th>
                <th class="border border-gray-300 px-4 py-3 text-center font-semibold">
                  5 (Excellent)
                </th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr class="hover:bg-purple-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-purple-100">
                  A. In-Depth Conversation with AI
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  No exchanges or chat history provided; no conversation beyond initial input; no
                  questions asked
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Sparse exchanges with incomplete or no chat history; basic conversation with one
                  or two simple questions; lacks depth
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Adequate exchanges shown in chat history; moderate conversation with some relevant
                  questions; shows some depth
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Robust exchanges with comprehensive chat history; in-depth conversation with
                  detailed, relevant questions on all levels
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Extensive exchanges with thorough, well-documented chat history; highly in-depth
                  conversation with insightful, multi-level questions
                </td>
              </tr>
              <tr class="hover:bg-purple-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-purple-100">
                  B. Critical Review of AI Suggestions
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  All AI suggestions accepted without evaluation; no critical thought
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Most AI suggestions accepted with little critical analysis
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Some AI suggestions evaluated; partial critical review with justification
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Most AI suggestions critically assessed; clear justification for choices
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  All AI suggestions thoroughly evaluated; strong, evidence-based justification
                </td>
              </tr>
              <tr class="hover:bg-purple-50 transition-colors">
                <td class="border border-gray-300 px-4 py-3 font-medium bg-purple-100">
                  C. Refining Process
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">No revisions made</td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Minimal revisions with no iterative process
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Some revisions with limited iteration based on AI feedback
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Clear iterative process with multiple revisions based on AI input
                </td>
                <td class="border border-gray-300 px-4 py-3 text-gray-700">
                  Extensive refinement with critical review of AI feedback at each step
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Toggle state management
const sections = ref({
  teachers: false,
  students: false,
  context: false
})

// Toggle section function
const toggleSection = (section) => {
  sections.value[section] = !sections.value[section]
}
</script>
