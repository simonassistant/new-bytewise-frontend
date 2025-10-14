import { ref, computed, onMounted, nextTick } from "vue"
import { useRouter } from "vue-router"
import { useChatbotStore } from "@/components/chatbotStore"
import { io } from "socket.io-client"
import { BASE_URL } from "@/components/base_url"
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk"
import { useAzureSpeech } from "./useAzureSpeech.js"
import { useNotifications } from "./useNotifications.js"

export function useChatLogic() {
  const router = useRouter()
  const chatbotStore = useChatbotStore()

  // --- State ---
  const chatHistory = ref([])
  const apiKey = ref("")
  const systemPrompt = ref("")
  const welcomePrompt = ref("")
  const model = ref("")
  const isConnected = ref(false)
  const isSidebarOpen = ref(true)
  const avatarState = ref("idle")
  const isRecording = ref(false)
  const isPlaying = ref(false)
  const isRecognizing = ref(false)
  const inputMode = ref("audio")
  const userText = ref("")
  const isLoading = ref(false)
  const showReport = ref(false)
  const selectedProvider = ref("openrouter")
  const isConnecting = ref(false)
  const notification = ref({ message: "", type: "success", visible: false })
  const messagesContainer = ref(null)
  const showAvatar = ref(true)

  let socket = null

  // --- External composables ---
  const { showNotification } = useNotifications(notification)
  const { getAzureToken, speakReplySequentially } = useAzureSpeech(avatarState, isPlaying)

  // --- Computeds ---
  const selectedBot = computed(() => chatbotStore.availableBots.find((b) => b.id === router.currentRoute.value.params.avatarId))
  const assistantCount = computed(() => chatHistory.value.filter((m) => m.role === "assistant").length)
  const userCount = computed(() => chatHistory.value.filter((m) => m.role === "user").length)
  const tokenUsage = computed(() => {
    let total = 0
    chatHistory.value.forEach((m, i) => {
      if (m.role === "user") total += m.content?.length || 0
      if (m.role === "assistant" && i !== 0) total += m.content?.length || 0
    })
    return Math.floor((total * 3) / 4)
  })

  // --- Lifecycle ---
  onMounted(async () => {
    await chatbotStore.loadBots()
    if (!selectedBot.value) {
      router.push("/")
      return
    }
    systemPrompt.value = selectedBot.value.systemPrompt
    welcomePrompt.value = selectedBot.value.welcomePrompt
    model.value = selectedBot.value.model
    await getAzureToken()

    const savedApiKey = localStorage.getItem("chatbot_api_key")
    if (savedApiKey) {
      apiKey.value = savedApiKey
      await connectAPI(true)
    }
  })

  // --- Core helpers ---
  function newMessage(role, content) {
    return { role, content, timestamp: new Date() }
  }

  function scrollToBottom() {
    nextTick(() => {
      const el = messagesContainer.value
      if (el) el.scrollTop = el.scrollHeight
    })
  }

  async function apiCall(endpoint, payload) {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res.json()
  }

  async function connectAPI(auto = false) {
    if (!apiKey.value && !auto && selectedProvider.value !== "openrouter") return
    localStorage.setItem("chatbot_api_key", apiKey.value)
    isConnecting.value = true
    isConnected.value = false

    try {
      const providerUrl = selectedProvider.value === "openrouter" ? "/chatbot/chat_openrouter" : "/chatbot/chat"
      const data = await apiCall(providerUrl, {
        chat_history: [
          { role: "system", content: "connection test" },
          { role: "user", content: "Hi" },
        ],
        api_key: apiKey.value,
        model_name: model.value,
      })
      const reply = data?.choices?.[0]?.message?.content || data?.response
      if (reply?.trim()) {
        isConnected.value = true
        showNotification("✅ Connected")
      } else showNotification("⚠️ No valid reply", "error")
    } catch (e) {
      console.error(e)
      showNotification("❌ Connection failed", "error")
    } finally {
      isConnecting.value = false
    }

    connectWebSocket()
    if (!chatHistory.value.length && isConnected.value) {
      chatHistory.value.push(newMessage("assistant", welcomePrompt.value))
      scrollToBottom()
    }
  }

  function connectWebSocket() {
    socket = io(`${BASE_URL}/streaming-avatar`, { transports: ["websocket"] })
  }

  async function sendTextToChatbot() {
    if (!isConnected.value || !userText.value.trim() || isLoading.value) return
    chatHistory.value.push(newMessage("user", userText.value))
    userText.value = ""
    chatHistory.value.push(newMessage("assistant", "⏳ Thinking..."))
    const idx = chatHistory.value.length - 1
    isLoading.value = true
    avatarState.value = "thinking"

    try {
      const providerUrl = selectedProvider.value === "openrouter" ? "/chatbot/chat_openrouter" : "/chatbot/chat"
      const data = await apiCall(providerUrl, {
        chat_history: chatHistory.value.map(({ role, content }) => ({ role, content })),
        api_key: apiKey.value,
        model_name: model.value,
      })
      const reply = data?.choices?.[0]?.message?.content || "[No response]"
      chatHistory.value[idx] = newMessage("assistant", reply)
      await speakReplySequentially(reply)
    } catch (e) {
      console.error(e)
      chatHistory.value[idx] = newMessage("assistant", "❌ Error")
    } finally {
      isLoading.value = false
      avatarState.value = "idle"
    }
  }

  return {
    selectedBot,
    chatHistory,
    tokenUsage,
    userCount,
    assistantCount,
    connectAPI,
    sendTextToChatbot,
    showNotification,
    isConnected,
    isLoading,
    isSidebarOpen,
    apiKey,
    model,
    avatarState,
    showAvatar,
    inputMode,
    userText,
    toggleRecording: () => { /* later we can extract STT here */ }
  }
}