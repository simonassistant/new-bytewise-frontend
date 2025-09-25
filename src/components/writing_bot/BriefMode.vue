<template>
  <div class="space-y-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Writing Assessment Tasks</h1>
      <p class="text-gray-600">Detailed rubrics and guidelines for assessment</p>
    </div>

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
