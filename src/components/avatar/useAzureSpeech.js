import { ref } from "vue";
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk";

/**
 * Handles Azure TTS (Text-to-Speech) and STT (Speech-to-Text)
 * Uses user-provided subscription key stored in localStorage for security.
 */
export function useAzureSpeech(showNotification) {
    const isRecording = ref(false);
    const isPlaying = ref(false);
    const avatarState = ref("idle");
    const avatarGender = ref("male");
    const azureSpeechKey = ref(localStorage.getItem("azure_speech_key") || "");
    const azureSpeechRegion = ref(localStorage.getItem("azure_speech_region") || "eastasia");

    function setAzureCredentials(key, region) {
        azureSpeechKey.value = key;
        azureSpeechRegion.value = region || "eastasia";
        localStorage.setItem("azure_speech_key", key);
        localStorage.setItem("azure_speech_region", azureSpeechRegion.value);
    }

    function clearAzureCredentials() {
        azureSpeechKey.value = "";
        azureSpeechRegion.value = "eastasia";
        localStorage.removeItem("azure_speech_key");
        localStorage.removeItem("azure_speech_region");
    }

    function getAzureConfig() {
        if (!azureSpeechKey.value) {
            return { subscriptionKey: null, region: null };
        }
        return { subscriptionKey: azureSpeechKey.value, region: azureSpeechRegion.value };
    }

    function isAzureConfigured() {
        return !!azureSpeechKey.value;
    }

    // --- TTS (Speech Synthesis) ---
    function splitIntoSentences(text) {
        return text.replace(/\s+/g, " ").match(/[^.!?]+[.!?]+/g) || [text];
    }

    async function synthesizeToBuffer(sentence) {
        const config = getAzureConfig();
        if (!config.subscriptionKey) throw new Error("Azure Speech key not configured");

        const speechConfig = speechsdk.SpeechConfig.fromSubscription(
            config.subscriptionKey,
            config.region
        );
        return new Promise((resolve, reject) => {
            const pushStream = speechsdk.AudioOutputStream.createPullStream();
            const audioConfig = speechsdk.AudioConfig.fromStreamOutput(pushStream);
            const synthesizer = new speechsdk.SpeechSynthesizer(speechConfig, audioConfig);
            (avatarGender.value == "female")
            const voiceName =
                avatarGender.value === "female"
                    ? "en-US-JennyNeural"
                    : "en-US-GuyNeural";

            const ssml = `
                            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                                <voice name="${voiceName}">
                                <prosody rate="-8%" pitch="-10%">
                                    ${sentence}
                                </prosody>
                                </voice>
                            </speak>`;
            synthesizer.speakSsmlAsync(
                ssml,
                (result) => {
                    synthesizer.close();
                    if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
                        resolve(result.audioData);
                    } else {
                        reject(result.errorDetails);
                    }
                },
                (err) => {
                    synthesizer.close();
                    reject(err);
                }
            );
        });
    }

    function playAudioBuffer(buffer) {
        return new Promise((resolve) => {
            const blob = new Blob([buffer], { type: "audio/wav" });
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.onended = () => {
                URL.revokeObjectURL(url);
                resolve();
            };
            audio.play();
        });
    }

    /**
     * Synthesize and play text sequentially sentence by sentence.
     */
    async function speakReplySequentially(replyText) {
        const sentences = splitIntoSentences(replyText);
        isPlaying.value = true;

        try {
            let chain = Promise.resolve();
            for (const sentence of sentences) {
                const synthPromise = synthesizeToBuffer(sentence);
                chain = chain.then(async () => {
                    try {
                        const buffer = await synthPromise;

                        avatarState.value = "speaking";
                        await playAudioBuffer(buffer);
                    } catch (err) {
                        console.error("TTS sentence error:", err);
                    }
                });
            }
            await chain;
        } catch (err) {
            console.error("Pipeline TTS error:", err);
        } finally {
            isPlaying.value = false;
            avatarState.value = "idle";
        }
    }


    // --- STT (Speech Recognition) ---
    async function startRecording(sendRecognizedText) {
        if (isRecording.value) return;
        try {
            const config = getAzureConfig();
            if (!config.subscriptionKey) {
                showNotification?.("❌ Azure Speech key not configured", "error");
                return;
            }

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaStreamRef.value = stream;

            const speechConfig = speechsdk.SpeechConfig.fromSubscription(
                config.subscriptionKey,
                config.region
            );
            speechConfig.speechRecognitionLanguage = "en-US";

            const audioConfig = speechsdk.AudioConfig.fromDefaultMicrophoneInput();
            recognizerRef.value = new speechsdk.SpeechRecognizer(speechConfig, audioConfig);

            isRecording.value = true;
            avatarState.value = "listening";

            recognizerRef.value.startContinuousRecognitionAsync();

            recognizerRef.value.recognized = (s, e) => {
                if (e.result.reason === speechsdk.ResultReason.RecognizedSpeech) {
                    recognizedTextBuffer.value += e.result.text + " ";
                }
            };

            recognizerRef.value.canceled = (s, e) => {
                console.warn("Recognition canceled:", e);
            };

            recognizerRef.value.sessionStopped = () => {
                stopRecordingInternal(sendRecognizedText);
            };

        } catch (err) {
            console.error("Azure STT error:", err);
            showNotification?.("❌ Speech recognition failed", "error");
            resetRecordingState();
        }
    }

    function stopRecordingInternal(sendRecognizedText) {
        if (!isRecording.value) return;

        recognizerRef.value?.stopContinuousRecognitionAsync(() => {
            const recognizedText = recognizedTextBuffer.value.trim();
            if (recognizedText && sendRecognizedText) sendRecognizedText(recognizedText);
            resetRecordingState();
        });
        mediaStreamRef.value?.getTracks().forEach((t) => t.stop());
    }

    function resetRecordingState() {
        isRecording.value = false;
        avatarState.value = "idle";
        recognizedTextBuffer.value = "";
        recognizerRef.value = null;
        mediaStreamRef.value = null;
    }

    // Refs for internal management
    const recognizerRef = ref(null);
    const mediaStreamRef = ref(null);
    const recognizedTextBuffer = ref("");

    // Compose an object similar to your previous toggleRecording prefix
    const toggleRecording = {
        start: startRecording,
        stop: stopRecordingInternal
    };

    return {
        isRecording,
        isPlaying,
        avatarState,
        avatarGender,
        azureSpeechKey,
        azureSpeechRegion,
        getAzureConfig,
        setAzureCredentials,
        clearAzureCredentials,
        isAzureConfigured,
        speakReplySequentially,
        toggleRecording,
    };
}