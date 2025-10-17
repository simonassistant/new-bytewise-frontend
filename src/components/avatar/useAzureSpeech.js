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
    const isRecognizing = ref(false);
    const avatarState = ref("idle");

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
        speechConfig.speechSynthesisVoiceName = "en-US-JennyNeural";

        return new Promise((resolve, reject) => {
            const pushStream = speechsdk.AudioOutputStream.createPullStream();
            const audioConfig = speechsdk.AudioConfig.fromStreamOutput(pushStream);
            const synthesizer = new speechsdk.SpeechSynthesizer(speechConfig, audioConfig);

            synthesizer.speakTextAsync(
                sentence,
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
        avatarState.value = "speaking";

        try {
            let chain = Promise.resolve();
            for (const sentence of sentences) {
                const synthPromise = synthesizeToBuffer(sentence);
                chain = chain.then(async () => {
                    try {
                        const buffer = await synthPromise;
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
    async function toggleRecording(sendRecognizedText) {
        if (isRecording.value) {
            isRecording.value = false;
            avatarState.value = "idle";
            return;
        }
        try {
            const tokenObj = await getAzureToken();
            if (!tokenObj.authToken) {
                showNotification?.("❌ Could not get Azure token", "error");
                return;
            }

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            const chunks = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) chunks.push(e.data);
            };
            // When local recording stops, save & download
            mediaRecorder.onstop = () => {
                // const audioBlob = new Blob(chunks, { type: "audio/webm" });
                // const url = URL.createObjectURL(audioBlob);
                // // --- trigger file download ---
                // const a = document.createElement("a");
                // a.href = url;
                // a.download = `user_audio_${Date.now()}.webm`; // or .wav if you like
                // document.body.appendChild(a);
                // a.click();
                // document.body.removeChild(a);
                // URL.revokeObjectURL(url);
                // console.log("🎧 Audio file downloaded!");
            };

            mediaRecorder.start();
            isRecording.value = true;
            avatarState.value = "listening";
            isRecognizing.value = true;

            const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(
                tokenObj.authToken,
                tokenObj.region
            );
            speechConfig.speechRecognitionLanguage = "en-US";
            const audioConfig = speechsdk.AudioConfig.fromDefaultMicrophoneInput();
            const recognizer = new speechsdk.SpeechRecognizer(speechConfig, audioConfig);

            recognizer.recognizeOnceAsync((result) => {
                mediaRecorder.stop();
                stream.getTracks().forEach((t) => t.stop());
                isRecording.value = false;
                isRecognizing.value = false;
                avatarState.value = "thinking";
                if (result.reason === speechsdk.ResultReason.RecognizedSpeech) {
                    const recognizedText = result.text.trim();
                    if (recognizedText && sendRecognizedText) sendRecognizedText(recognizedText);
                } else {
                    showNotification?.("⚠️ Speech not recognized", "error");
                }
                recognizer.close();
            });
        } catch (err) {
            console.error("Azure STT error:", err);
            showNotification?.("❌ Speech recognition failed", "error");
            isRecording.value = false;
            isRecognizing.value = false;
            avatarState.value = "idle";
        }
    }

    return {
        // state
        isRecording,
        isPlaying,
        isRecognizing,
        avatarState,

        // methods
        getAzureToken,
        speakReplySequentially,
        toggleRecording,
    };
}