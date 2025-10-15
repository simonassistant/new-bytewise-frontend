// src/composables/useChatFunctions.js
import { BASE_URL } from "@/components/base_url";
import { Assessment_Mode_Prompt, Trainging_Mode_Prompt } from "@/components/writing_bot/promptAndEssay.js";

export function useChatFunctions({
    userMessage,
    currentMode,
    activeChatHistory,
    originalDraft,
    finalDraft,
    isConnected,
    apiKey,
    model,
    isThinking,
    isOriginalDraftConfirmed,
    isUpdatingDraft,
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
                if (currentMode.value === "training" || isOriginalDraftConfirmed.value) {
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

        let payloadHistory = [
            {
                role: "system",
                content:
                    "Extract the full revised essay from the latest assistant message. If no changes were made, reply 'no changes were made'. Always provide the complete revised text only. Do not include any explanations or additional text.\n\n" +
                    "Original Draft:\n---\n" +
                    `${originalDraft.value || "(empty)"}\n---\n\n` +
                    "Chat History:\n" +
                    activeChatHistory.value
                        .map((msg) => `${msg.role === "user" ? "User" : "AI"}: ${msg.content}`)
                        .join("\n"),
            },
        ];

        try {
            const reply = await talkToChatbot(payloadHistory);
            if (reply && !(reply.toLowerCase().includes("no changes") && reply.trim().length < 25)) {
                finalDraft.value = reply.trim();
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