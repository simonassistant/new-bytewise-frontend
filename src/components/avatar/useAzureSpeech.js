import { ref } from "vue";
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk";
import { BASE_URL } from "@/components/base_url";

/**
 * Handles Azure TTS (Text-to-Speech) and STT (Speech-to-Text)
 * Includes token management and utility helpers.
 */
export function useAzureSpeech(showNotification) {
    // --- State ---
    const isRecording = ref(false);
    const isPlaying = ref(false);
    const avatarState = ref("idle");
    const avatarGender = ref("male");
    // --- Token helpers ---
    function setCookie(name, value, minutes) {
        const d = new Date();
        d.setTime(d.getTime() + minutes * 60 * 1000);
        const expires = "expires=" + d.toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)};${expires};path=/`;
    }

    function getCookie(name) {
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookies = decodedCookie.split("; ");
        for (let cookie of cookies) {
            const [key, value] = cookie.split("=");
            if (key === name) return value;
        }
        return null;
    }

    /**
     * Fetch or retrieve cached Azure token and region
     */
    async function getAzureToken() {
        const cachedToken = getCookie("azureToken");
        const cachedRegion = getCookie("azureRegion");
        if (cachedToken && cachedRegion) {
            return { authToken: cachedToken, region: cachedRegion };
        }
        try {
            const res = await fetch(`${BASE_URL}/streaming-avatar/get-speech-token`);
            if (!res.ok) throw new Error("Failed to fetch Azure speech token");
            const data = await res.json();
            setCookie("azureToken", data.token, 9);
            setCookie("azureRegion", data.region, 9);
            return { authToken: data.token, region: data.region };
        } catch (err) {
            console.error("Azure token fetch error:", err);
            return { authToken: null, region: null };
        }
    }

    // --- TTS (Speech Synthesis) ---
    function splitIntoSentences(text) {
        return text.replace(/\s+/g, " ").match(/[^.!?]+[.!?]+/g) || [text];
    }

    async function synthesizeToBuffer(sentence) {
        const tokenObj = await getAzureToken();
        if (!tokenObj.authToken) throw new Error("No Azure token");

        const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(
            tokenObj.authToken,
            tokenObj.region
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
            const tokenObj = await getAzureToken();
            if (!tokenObj.authToken) {
                showNotification?.("❌ Could not get Azure token", "error");
                return;
            }

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaStreamRef.value = stream;

            const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(
                tokenObj.authToken,
                tokenObj.region
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
        // state
        isRecording,
        isPlaying,
        avatarState,
        avatarGender,
        // methods
        getAzureToken,
        speakReplySequentially,
        toggleRecording,
    };
}