# new_EEGC Components Overview

This folder powers the LANG 0036 AI writing collaboration experience surfaced through the `NewEEGC.vue` view. Each file contributes a different part of the briefing, chat-based revision workflow, or reporting flow:

- `BackgroundAndRubrics.vue` – Form-driven editor that collects course details, student context, and rubric text, and emits updates once everything is ready for AI sharing.
- `BriefMode.vue` – Minimal wrapper that embeds the static `briefing.html` guidance inside an iframe for quick reference.
- `BriefMode copy.vue` – Currently not in use, just kept for reference.
- `ChatInterface.vue` – Main two-column workspace combining chat history, message input, bullet-point summaries, and original/final draft editors with confirmation gates per mode.
- `CourseHeader.vue` – Header banner introducing the LANG 0036 lab and reminding students to submit their chat history.
- `ModeSelector.vue` – Button group controller that toggles briefing, training, and assessment states while surfacing status badges.
- `SkillesDeveloped.vue` – Dashboard mock-up that visualises collaboration skills and session statistics via reusable badge/stat subcomponents.
- `WritingBotReport.vue` – Modal that renders assessment reports, supports markdown/PDF exports, and lets students email results.
- `promptAndEssay.js` – Prompt templates, greeting text, and sample essay content injected into conversations and assessment pipelines.
- `useChatFunctions.js` – Composition utility that wraps API calls, builds mode-aware system prompts, tracks chat history, and keeps bullet points in sync.

`NewEEGC.vue` orchestrates these modules, managing mode-specific drafts, API connectivity, and report generation for the overall experience.