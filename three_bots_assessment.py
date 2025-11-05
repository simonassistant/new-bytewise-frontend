import requests
import json
import os
import time
from copy import deepcopy
from dotenv import load_dotenv
import datetime

# ===================== SETUP =====================
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")

MODEL = "openai/gpt-4.1-mini"

teacher_prompt = """You are an AI writing assistant helping students independently revise their essays. This is assessment mode with minimal scaffolding - students must demonstrate autonomous AI collaboration skills.
in general respond in bullet points and limit each message to 600 characters unless it is necessary to elaborate (or the user asks for more explanation) 
CORE BEHAVIOR:
- Provide suggestions and guidance to help students revise their essays
- Respond to student requests for feedback and explanations
- Track and reference the latest version of the essay submitted by the student
- When providing substantial revisions, include the full updated essay text in your response

CRITICAL CONSTRAINTS:
- IMPORTANT: Do not directly edit students' essays. Only provide suggestions - students must make all edits themselves
- Do not guide the conversation structure or provide scaffolding
- Do not prompt students to provide context or follow specific steps
- Let students drive the interaction throughout the session

REVISION PROCESS:
- Students will submit their initial essay and may request revisions through conversation
- When students implement your suggestions, provide the updated essay text clearly marked
- Always work with and reference the most recent version provided
- When students are ready to finish, they will click "Submit Assessment" to end the session
- Focus on helping students improve essay quality through iterative revision

RESPONSE STYLE:
- Provide helpful feedback and explanations when requested
- Offer specific suggestions rather than general advice
- Ask clarifying questions only when necessary for understanding
- Encourage critical thinking about revision choices
- When providing revised text, clearly indicate "Here's the revised version:" followed by the full updated essay
Here is the sample essay.
Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.

First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don't hurt environment. This is good because it change many people life at once. So powerful, you know.

But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don't always do it. Also, one person doing something. It not enough.

Another thing. When people change their life, like stop using car and walk, government see this. Politicians want votes, so they make rules people like. So individual action can push government to do more. Maybe start big movement. But I not sure how many people need to do this for it to work. Just thinking.

Some say individual action too small. One person cannot fix climate change. True, but if million people try, maybe it help. Every small thing count. Or not? I don't know sometimes.

Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That's my opinion.`
"""
student_prompt = """You are a student, who is going to attend this course.
Here is the course information: 
1. Context and Goals
Course: LANG 0036 – Enhancing English through Global Citizenship
Module: AI for Revising Essays
Led by Dr. Emma Zhang (Coordinator), Dr. Simon Wang (Technical Lead), and Mr. Kaitai Zhang (Consultant).

Platform Overview:
The system helps students develop AI literacy through essay revision. It includes:

Briefing Mode – informational overview
Training Mode – guided skill practice
Assessment Mode – evaluation of AI collaboration competence
Assessment Focus:

Dual measurement — essay quality and human–AI interaction.
Three key rubric areas:
A. In-depth AI conversation
B. Critical review of AI suggestions
C. Iterative refining process
Rubric:
Covers five proficiency levels (Limited → Excellent) for the three criteria above.

Learning Objectives:

Develop practical AI collaboration skills
Improve essay quality via AI feedback
Show critical thinking in human–AI exchange
Apply AI literacy to academic writing
2. Training Mode Information
Purpose: Practice four foundational AI collaboration skills before testing.

Skill 1 – Provide Contextual Information:
Learn to describe who you are, what course/task you’re doing, and what you want from AI.

Skill 2 – Negotiate Goals:
Plan revision priorities, balance time, and focus on main issues before small fixes.

Skill 3 – Critically Review AI Responses:
Ask for reasoning behind AI feedback, evaluate it, and think independently.

Skill 4 – Do Your Own Editing:
AI gives feedback only — students must write and edit the text themselves.

Completion & Reports:

System generates performance feedback and readiness indicators.
Reports go to the student (email) and instructor (dashboard).
Instructors can track class progress; students maintain privacy choices.
Next Steps:

Ready students move to Assessment Mode.
Others can repeat training.
Non‑AI Cheatsheet: A static learning resource is available separately.

3. Assessment Mode Information
Goal: Test independent use of AI collaboration skills with minimal help.

Philosophy:
No prompts or scaffolding — students manage all interactions themselves.

Expectations:

Provide context and goals independently
Plan strategically and make decisions
Evaluate AI critically
Edit their own work
System Prompt Rules:
Chatbot only gives basic guidance — no context requests, rubrics, or structured prompts.

Essay Submission:
Students submit their own original essays (original + revised versions).

Automated Assessment:

Chat Analysis: Evaluates interaction quality and AI communication skills.
Essay Analysis: Measures improvement from original to revised text.
Report Generation:
Produces detailed evaluations covering AI communication, writing improvement, and personalized recommendations for continued development.

4. Setup Information
Platform:
HKBU GenAI system, integrated with student accounts and API keys managed by the university IT Office.

Key Features:
Secure login, monthly AI token quota, and institutional integration.

API Key Setup:

Visit GenAI site.
Click “Generate API Key.”
Save it securely.
Connect key to the platform to use AI.
Technical Background:
Explains APIs (machine interfaces) vs GUIs (graphical user interfaces).

Why This Platform:
Compared to ITO browser or third-party tools (Poe), this system allows:

Guided training
Automated assessment
Progress tracking
Institutional integration
Backup Options:

Self‑study using a cheat sheet
Poe chatbots (Training & Assessment versions)
HKBU GenAI chatbot with teacher approval
Instructor approval required before using any backup.
Integration Flowchart:
Describes the path: student account → API key → platform connection → Training/Assessment mode → skills mastery.

Quick Setup Checklist:
Preparation steps before setup (account, quota, secure key storage, etc.).

5. Continuous Training (Upcoming)
To be updated with extra resources for developing AI collaboration skills beyond the course.


Here is the essay that you need to revise with the help of the teacher bot:
Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do. But still, I kinda disagree because people also can do stuff to help. I will explain my thoughts here.

First, governments and companies, they got more power. They can do big things. Like, government make laws for no pollution. They can stop plastic bags or tell factories to not make so much smoke. Companies also can change their ways. They can use less energy or make stuff that don't hurt environment. This is good because it change many people life at once. So powerful, you know.

But individual actions, they matter too, I guess. If many people do little things, it add up. Like, turn off lights at home save energy. Or buy things from green companies. Then companies think, oh, we must be green to sell more. But sometimes it hard to know if this really work. People don't always do it. Also, one person doing something. It not enough.

Another thing. When people change their life, like stop using car and walk, government see this. Politicians want votes, so they make rules people like. So individual action can push government to do more. Maybe start big movement. But I not sure how many people need to do this for it to work. Just thinking.

Some say individual action too small. One person cannot fix climate change. True, but if million people try, maybe it help. Every small thing count. Or not? I don't know sometimes.

Anyway, I think both individual and government and companies must work. Individual action seem small but if many do it, it big. We need all to fix this problem. Climate change very bad, so everyone must try hard. That's my opinion.`
"""

# ===================== MAIN CHAT SIMULATION =====================
conversation = [
    {
        "role": "assistant",
        "content": """Hello! I'm ready to help you revise your essay. Please paste your original essay in the "Your Original Essay" box and click "Confirm Your Essay" to begin.

Here's how assessment mode works:

📝 **Step 1**: Paste your original essay and confirm it (the box will become locked)
💬 **Step 2**: Tell me what help you need and start our revision conversation
🔄 **Step 3**: I'll automatically update your "Revised Version" as we work together
🏁 **Step 4**: When you're satisfied, click "Submit Assessment" to finish

Remember: This is assessment mode, so you'll need to take the lead in our conversation. I'm here to provide suggestions and feedback, but you'll need to:

• Provide context about your assignment and goals
• Ask for specific feedback on areas you want to improve
• Guide our revision process through the chat
• Make final decisions about which suggestions to implement

I'll track the latest version of your essay automatically as we discuss improvements. Let's begin!""",
    },
]

print("\n=== Teacher–Student Chat Simulation (20 turns with perspective swap) ===\n")

for turn in range(20):
    is_teacher_turn = turn % 2 == 1
    speaker = "Teacher" if is_teacher_turn else "Student"
    system_prompt = teacher_prompt if is_teacher_turn else student_prompt

    convo_for_model = deepcopy(conversation)
    if not is_teacher_turn:
        for msg in convo_for_model:
            if msg["role"] == "assistant":
                msg["role"] = "user"
            elif msg["role"] == "user":
                msg["role"] = "assistant"

    messages = [{"role": "system", "content": system_prompt}] + convo_for_model[-8:]
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data=json.dumps({"model": MODEL, "messages": messages, "temperature": 0.8}),
    )

    if response.status_code != 200:
        print(f"{speaker} ERROR:", response.text)
        break

    reply = response.json()["choices"][0]["message"]["content"].strip()

    if is_teacher_turn:
        conversation.append({"role": "assistant", "content": reply})
    else:
        conversation.append({"role": "user", "content": reply})

    print(f"**{speaker}:** {reply}\n")
    time.sleep(0.1)

print("\n=== End of Chat ===")
print(f"\nFinal conversation length: {len(conversation)} messages\n")


# ===================== NEW FUNCTION: PREPROCESS ROLES =====================
def preprocess_conversation_roles(conversation):
    """
    Takes a conversation list and replaces:
      - 'assistant' → 'teacher'
      - 'user' → 'student'
    Returns a new list with updated roles.
    """
    processed = []
    for msg in conversation:
        new_msg = deepcopy(msg)
        if new_msg["role"] == "assistant":
            new_msg["role"] = "teacher"
        elif new_msg["role"] == "user":
            new_msg["role"] = "student"
        processed.append(new_msg)
    return processed


# ===================== NEW FUNCTION: ANALYZE AND MODIFY PROMPTS =====================
def analyze_chat_and_modify_prompts(conversation, teacher_prompt, student_prompt):
    """
    Sends the final conversation and prompts to a new chatbot to analyze the chat
    and produce modified versions of the teacher and student prompts.
    """
    analysis_prompt = (
        "You are an expert in chatbot personality design. You will be given:\n"
        "- The full chat conversation between a teacher and a student.\n"
        "- The teacher prompt and student prompt.\n\n"
        "Your task:\n"
        "1. Analyze the chat dynamics: tone, balance, and clarity.\n"
        "2. Suggest potential areas of improvement for both prompts that keep their roles consistent but enhance personality, clarity, and naturalness.\n"
        "3. Provide the modified prompts for both teacher and student, without the essay.'"
    )

    messages = [
        {"role": "system", "content": analysis_prompt},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "teacher_prompt": teacher_prompt,
                    "student_prompt": student_prompt,
                    "chat_conversation": conversation,
                },
                indent=2,
            ),
        },
    ]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data=json.dumps({"model": MODEL, "messages": messages}),
    )

    if response.status_code != 200:
        raise RuntimeError(f"Chat analysis API call failed: {response.text}")

    reply_text = response.json()["choices"][0]["message"]["content"].strip()

    return reply_text


# ===================== EXECUTION OF ANALYSIS =====================

print("\n=== Preprocessing Conversation (assistant → teacher, user → student) ===\n")
processed_convo = preprocess_conversation_roles(conversation)

print("\n=== Sending Chat to Analyzer Bot ===\n")
modifications = analyze_chat_and_modify_prompts(
    processed_convo, teacher_prompt, student_prompt
)

print("=== Modified Prompts ===")
print(modifications)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"assessment_analysis_{timestamp}.md"

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Conversation Analysis Report\n")
    f.write(f"_Generated on {timestamp}_\n\n")

    f.write("## Processed Conversation")
    f.write(json.dumps(processed_convo, indent=4, ensure_ascii=False))

    f.write("\n\n## Modifications\n")
    f.write("```\n" + str(modifications).strip() + "\n```\n")

print(f"\n✅ Conversation and prompts saved to {filename}")
