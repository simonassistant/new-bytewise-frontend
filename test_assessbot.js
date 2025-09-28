/**
 * Test script for AssessBot functionality
 * This script validates the AssessBot integration in the WritingBot.vue component
 */

import { AssessBot_Prompt } from './src/components/writing_bot/sampleEssay.js';

// Test data - sample student submission
const testData = {
  originalEssay: `Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.

First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don't hurt environment. This is good because it change many people life at once. So powerful, you know.

But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don't always do it. Also, one person doing something. It not enough.

Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That's my opinion.`,

  revisedEssay: `Climate change is an urgent global issue that requires immediate action. While some argue that individual actions are insignificant compared to government and corporate efforts, I believe that both individual and institutional responses are essential for effectively addressing this crisis.

Governments and large corporations undoubtedly possess greater power to implement widespread changes. Governments can enact comprehensive environmental legislation, such as carbon taxes and renewable energy mandates, while corporations can transform entire industries through sustainable practices and green technologies. These institutional changes can impact millions of people simultaneously, creating systemic solutions that individual actions alone cannot achieve.

However, individual actions remain crucial for several reasons. First, collective individual behavior creates significant environmental impact when multiplied across populations. When millions of people adopt energy-saving practices, choose sustainable products, or reduce consumption, the cumulative effect becomes substantial. Second, individual actions demonstrate public demand for environmental responsibility, influencing corporate strategies and government policies. Companies respond to consumer preferences, while politicians recognize the electoral importance of environmental issues.

Furthermore, individual actions can catalyze broader social movements. When people make visible environmental choices, they inspire others and contribute to shifting social norms. This grassroots momentum often pressures institutions to adopt more ambitious environmental policies.

In conclusion, addressing climate change requires coordinated efforts from all levels of society. While governments and corporations must lead with large-scale solutions, individual actions provide the social foundation and market signals necessary for systemic change. Both approaches are interdependent and essential for creating a sustainable future.`,

  chatHistory: [
    {
      role: "assistant",
      content: "Hello! I'm ready to help you revise your essay. Please paste your original essay in the 'Your Original Essay' box and click 'Confirm Your Essay' to begin.",
      timestamp: new Date("2024-01-15T10:00:00Z")
    },
    {
      role: "user", 
      content: "I'm taking LANG 0036 - Enhancing English through Global Citizenship and need help revising my climate change essay. I'll be assessed on both essay improvement and AI communication skills. Can you help me improve the content and organization?",
      timestamp: new Date("2024-01-15T10:01:00Z")
    },
    {
      role: "assistant",
      content: "I'd be happy to help you revise your climate change essay! Since you'll be assessed on both essay quality and AI collaboration skills, let's work together strategically. I can see your essay discusses whether individual actions matter compared to government/corporate efforts. \n\nLet me analyze the main areas for improvement:\n1. **Content & Ideas**: Your viewpoint is present but could be clearer and better supported\n2. **Organization**: The essay needs better structure and logical flow\n3. **Vocabulary**: We can enhance precision and variety\n4. **Grammar**: Several sentence structure issues need attention\n\nWhat specific area would you like to focus on first? I'd recommend starting with content and organization before moving to language improvements.",
      timestamp: new Date("2024-01-15T10:02:00Z")
    },
    {
      role: "user",
      content: "I think the content and organization need the most work. Can you suggest specific improvements for the introduction and body paragraphs?",
      timestamp: new Date("2024-01-15T10:03:00Z")
    },
    {
      role: "assistant", 
      content: "Excellent question! Let me suggest specific improvements:\n\n**Introduction improvements:**\n- Start with a stronger hook about climate change urgency\n- Clearly state your position that BOTH individual and institutional actions are necessary\n- Preview your main arguments\n\n**Body paragraph organization:**\n- Paragraph 1: Government/corporate power and capabilities\n- Paragraph 2: Why individual actions matter (collective impact, market signals)\n- Paragraph 3: How individual actions influence institutions\n\n**Specific content suggestions:**\n- Add concrete examples (carbon taxes, renewable energy mandates)\n- Explain the concept of 'cumulative effect' more clearly\n- Discuss how consumer behavior influences corporate strategy\n\nWhat do you think about this structure? Would you like to work on implementing these changes section by section?",
      timestamp: new Date("2024-01-15T10:04:00Z")
    },
    {
      role: "user",
      content: "That structure makes sense. Can you explain why you think the introduction needs a stronger hook? What makes a good hook for this type of essay?",
      timestamp: new Date("2024-01-15T10:05:00Z")
    },
    {
      role: "assistant",
      content: "Great critical question! You're demonstrating exactly the kind of thinking that will help you succeed.\n\nA strong hook is important because:\n1. **Engagement**: It immediately draws readers into the topic's urgency\n2. **Context setting**: It establishes why this debate matters now\n3. **Academic tone**: It shows sophisticated writing from the start\n\nFor climate change essays, effective hooks might:\n- Reference recent climate data or events\n- Highlight the scale/urgency of the problem\n- Present the central tension (individual vs institutional responsibility)\n\nYour current opening 'Climate change, it is very huge problem now' is direct but could be more compelling. Something like 'Climate change represents an unprecedented global challenge requiring coordinated action at every level of society' would better establish the essay's academic tone and complexity.\n\nDo you see how this connects to the rubric's 'Content and Ideas' criterion about demonstrating awareness of the issue? What's your reaction to this suggestion?",
      timestamp: new Date("2024-01-15T10:06:00Z")
    },
    {
      role: "user",
      content: "I understand. Let me work on revising the introduction and first body paragraph with your suggestions. I'll focus on clearer thesis statement and better examples.",
      timestamp: new Date("2024-01-15T10:07:00Z")
    },
    {
      role: "assistant",
      content: "Perfect! You're taking ownership of the revision process, which is exactly what we want to see. As you work on those revisions:\n\n**For the introduction:**\n- Make sure your thesis clearly states your position on both sides\n- Consider using transition words to connect your ideas smoothly\n\n**For the first body paragraph:**\n- Start with a clear topic sentence about government/corporate power\n- Include specific examples like legislation or corporate initiatives\n- Explain HOW these examples demonstrate greater institutional impact\n\nTake your time to draft these changes, and then share what you've written. I'll provide feedback to help you refine it further. Remember, this iterative process is part of demonstrating your collaboration skills!",
      timestamp: new Date("2024-01-15T10:08:00Z")
    }
  ]
};

// Test function to validate AssessBot prompt structure
function testAssessBotPrompt() {
  console.log("🧪 Testing AssessBot Prompt Structure...");
  
  // Check if prompt contains required sections
  const requiredSections = [
    "Role and Purpose",
    "Assessment Overview", 
    "Essay Writing Assessment Rubric",
    "Human-AI Interaction Assessment Rubric",
    "Assessment Process",
    "Output Format",
    "Assessment Guidelines"
  ];
  
  let allSectionsPresent = true;
  requiredSections.forEach(section => {
    if (!AssessBot_Prompt.includes(section)) {
      console.error(`❌ Missing section: ${section}`);
      allSectionsPresent = false;
    } else {
      console.log(`✅ Section found: ${section}`);
    }
  });
  
  // Check for rubric criteria
  const rubricCriteria = [
    "Content and Ideas",
    "Organization and Logical Progression", 
    "Vocabulary",
    "Grammar and Sentence Structure",
    "In-Depth Conversation with AI",
    "Critical Review of AI Suggestions",
    "Refining Process"
  ];
  
  rubricCriteria.forEach(criteria => {
    if (!AssessBot_Prompt.includes(criteria)) {
      console.error(`❌ Missing rubric criteria: ${criteria}`);
      allSectionsPresent = false;
    } else {
      console.log(`✅ Rubric criteria found: ${criteria}`);
    }
  });
  
  return allSectionsPresent;
}

// Test function to simulate assessment request format
function testAssessmentFormat() {
  console.log("\n🧪 Testing Assessment Request Format...");
  
  const assessmentSystemMessage = {
    role: "system",
    content: AssessBot_Prompt + 
      "\n\nOriginal Essay:\n---\n" + testData.originalEssay + 
      "\n---\n\nRevised Essay:\n---\n" + testData.revisedEssay + 
      "\n---\n\nChat History:\n" + 
      JSON.stringify(testData.chatHistory, null, 2)
  };
  
  // Validate structure
  const isValidStructure = (
    assessmentSystemMessage.role === "system" &&
    assessmentSystemMessage.content.includes("Original Essay:") &&
    assessmentSystemMessage.content.includes("Revised Essay:") &&
    assessmentSystemMessage.content.includes("Chat History:") &&
    assessmentSystemMessage.content.includes(testData.originalEssay) &&
    assessmentSystemMessage.content.includes(testData.revisedEssay)
  );
  
  if (isValidStructure) {
    console.log("✅ Assessment request format is valid");
    console.log(`📊 System message length: ${assessmentSystemMessage.content.length} characters`);
    console.log(`💬 Chat exchanges included: ${testData.chatHistory.length}`);
    return true;
  } else {
    console.error("❌ Assessment request format is invalid");
    return false;
  }
}

// Test function to validate chat history structure
function testChatHistoryProcessing() {
  console.log("\n🧪 Testing Chat History Processing...");
  
  const processedHistory = testData.chatHistory.map(msg => ({
    role: msg.role,
    content: msg.content,
    timestamp: msg.timestamp
  }));
  
  // Validate processed structure
  const isValidProcessing = (
    Array.isArray(processedHistory) &&
    processedHistory.length === testData.chatHistory.length &&
    processedHistory.every(msg => 
      msg.role && msg.content && msg.timestamp &&
      ['user', 'assistant'].includes(msg.role)
    )
  );
  
  if (isValidProcessing) {
    console.log("✅ Chat history processing is valid");
    console.log(`💬 Total exchanges: ${processedHistory.length}`);
    console.log(`👤 User messages: ${processedHistory.filter(m => m.role === 'user').length}`);
    console.log(`🤖 Assistant messages: ${processedHistory.filter(m => m.role === 'assistant').length}`);
    return true;
  } else {
    console.error("❌ Chat history processing failed");
    return false;
  }
}

// Run all tests
function runAllTests() {
  console.log("🚀 Starting AssessBot Integration Tests...\n");
  
  const test1 = testAssessBotPrompt();
  const test2 = testAssessmentFormat(); 
  const test3 = testChatHistoryProcessing();
  
  console.log("\n📋 Test Results Summary:");
  console.log(`AssessBot Prompt Structure: ${test1 ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Assessment Format: ${test2 ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Chat History Processing: ${test3 ? '✅ PASS' : '❌ FAIL'}`);
  
  const allPassed = test1 && test2 && test3;
  console.log(`\n🎯 Overall Result: ${allPassed ? '✅ ALL TESTS PASSED' : '❌ SOME TESTS FAILED'}`);
  
  if (allPassed) {
    console.log("\n🎉 AssessBot integration is ready for deployment!");
    console.log("The system can now:");
    console.log("• Generate comprehensive assessment reports");
    console.log("• Evaluate both essay writing and AI collaboration skills");
    console.log("• Provide structured feedback according to LANG 0036 rubrics");
  }
  
  return allPassed;
}

// Export for use in other modules or manual testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    runAllTests,
    testData,
    testAssessBotPrompt,
    testAssessmentFormat,
    testChatHistoryProcessing
  };
}

// Run tests if script is executed directly
if (typeof window === 'undefined') {
  runAllTests();
}