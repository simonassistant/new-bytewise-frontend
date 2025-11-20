// src/composables/useChatFunctions.js
import { BASE_URL } from "@/components/base_url";
import { Assessment_Mode_Prompt, Trainging_Mode_Prompt, BulletPoints_Generation_Prompt } from "@/components/new_EEGC/promptAndEssay.js";

export function useChatFunctions({
    userMessage,
    currentMode,
    activeChatHistory,
    originalDraft,
    finalDraft,
    bulletPoints,
    isConnected,
    apiKey,
    model,
    isThinking,
    isOriginalDraftConfirmed,
    isUpdatingDraft,
    courseInfo,
    courseInfoAssessment,
    currentTopic
}) {
    async function talkToChatbot(chat_history) {
        const res = await fetch(`${BASE_URL}/chatbot/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chat_history: chat_history,
                api_key: apiKey.value,
                model_name: model.value,
            }),
        });

        const data = await res.json();
        return data?.choices?.[0]?.message?.content || data?.response || data?.message || "";
    }

    async function sendMessage() {
        if (
            !userMessage.value.trim() ||
            isThinking.value ||
            !isConnected.value ||
            !apiKey.value
        )
            return;

        activeChatHistory.value.push({
            role: "user",
            content: userMessage.value,
            timestamp: new Date(),
        });
        userMessage.value = "";
        isThinking.value = true;

        try {
            let payloadHistory = [...activeChatHistory.value];

            if (currentMode.value === "assessment") {
                payloadHistory = [
                    {
                        role: "system",
                        content:
                            Assessment_Mode_Prompt +
                            "These are the student information details:\n" +
                            `Course Info: ${courseInfoAssessment.value || "(none)"}\n` +
                            `Current Topic: ${currentTopic.value || "(none)"}\n` +
                            "Original Draft:\n---\n" +
                            `${originalDraft.value || "(empty)"}\n---\n\n` +
                            "Current Revised Version:\n---\n" +
                            `${finalDraft.value || "(empty)"}\n---\n\n` +
                            "IMPORTANT: If the student makes specific edits or requests changes, provide the updated version of the essay in your response. Always include the full revised text when changes are made.",
                    },
                    ...payloadHistory,
                ];
            } else if (currentMode.value === "training") {
                payloadHistory = [
                    {
                        role: "system",
                        content:
                            Trainging_Mode_Prompt +
                            "These are the student information details:\n" +
                            `Course Info: ${courseInfo.value || "(none)"}\n` +
                            `Current Topic: ${currentTopic.value || "(none)"}\n` +
                            "Original Draft:\n---\n" +
                            `${originalDraft.value || "(empty)"}\n---\n\n` +
                            "Final Draft:\n---\n" +
                            `${finalDraft.value || "(empty)"}\n---\n\n`,
                    },
                    ...payloadHistory,
                ];
            }

            const reply = await talkToChatbot(payloadHistory);
            if (reply) {
                activeChatHistory.value.push({
                    role: "assistant",
                    content: reply,
                    timestamp: new Date(),
                });
                if (isOriginalDraftConfirmed.value) {
                    await extractAndUpdateEssay();
                }
            }
        } catch {
            activeChatHistory.value.push({
                role: "assistant",
                content: "⚠️ Error connecting to server.",
                timestamp: new Date(),
            });
        } finally {
            isThinking.value = false;
        }
    }

    async function extractAndUpdateEssay() {
        isUpdatingDraft.value = true;
        const refinedChatHistory = activeChatHistory.value.slice(-4);

        let payloadHistory = [
            {
                role: "system",
                content:
                    BulletPoints_Generation_Prompt +
                    refinedChatHistory
                        .map((msg) => `${msg.role === "user" ? "User" : "AI"}: ${msg.content}`)
                        .join("\n")
            },
        ];

        try {
            const reply = await talkToChatbot(payloadHistory);
            if (reply && reply.trim().length > 25) {
                bulletPoints.value = reply.trim();
            }
        } catch (error) {
            console.error("Error extracting essay:", error);
        } finally {
            isUpdatingDraft.value = false;
        }
    }

    return {
        sendMessage,
        talkToChatbot,
    };
}