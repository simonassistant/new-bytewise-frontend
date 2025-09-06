// composables/useChatbotConfig.js
import { ref, computed, watch } from 'vue';
import { ConfigurationManager } from '@/utils/ConfigurationManager';

let globalConfigManager = null;

export function useChatbotConfig(initialConfig = {}) {
  // Singleton pattern for configuration
  if (!globalConfigManager) {
    globalConfigManager = new ConfigurationManager();
    globalConfigManager.setupValidators();
  }
  
  const configManager = globalConfigManager;
  const isLoading = ref(false);
  const errors = ref([]);
  
  // Initialize with provided config
  if (Object.keys(initialConfig).length > 0) {
    try {
      configManager.updateConfig(initialConfig);
    } catch (error) {
      errors.value.push(error.message);
      console.error('Initial config validation failed:', error);
    }
  }
  
  // Reactive configuration
  const config = ref(configManager.getAll());
  
  // Computed derived values
  const themeConfig = computed(() => ({
    '--primary-color': config.value.primaryColor,
    '--secondary-color': config.value.secondaryColor,
    '--border-radius': config.value.borderRadius,
    '--font-family': config.value.fontFamily
  }));
  
  const apiConfig = computed(() => ({
    provider: config.value.apiProvider,
    endpoint: config.value.apiEndpoint,
    model: config.value.model,
    hasApiKey: !!config.value.apiKey
  }));
  
  const uiConfig = computed(() => ({
    theme: config.value.theme,
    size: config.value.size,
    enableVoice: config.value.enableVoice,
    enableTyping: config.value.enableTyping,
    enableEmail: config.value.enableEmail,
    autoResize: config.value.autoResize
  }));
  
  // Watch for configuration changes and sync
  const unsubscribe = configManager.observe((changes, origin) => {
    config.value = configManager.getAll();
    console.log('Configuration updated:', changes, 'from:', origin);
  });
  
  // Methods
  async function updateConfig(updates, origin = 'local') {
    isLoading.value = true;
    errors.value = [];
    
    try {
      const validUpdates = configManager.updateConfig(updates, origin);
      return validUpdates;
    } catch (error) {
      errors.value.push(error.message);
      throw error;
    } finally {
      isLoading.value = false;
    }
  }
  
  function resetConfig() {
    configManager.initializeDefaults();
    config.value = configManager.getAll();
  }
  
  function getApiKey() {
    return configManager.get('apiKey');
  }
  
  function exportConfig() {
    return configManager.exportConfig();
  }
  
  async function importConfig(configJson, origin = 'import') {
    return updateConfig(JSON.parse(configJson), origin);
  }
  
  // Theme utilities
  function applyTheme() {
    const root = document.documentElement;
    const theme = themeConfig.value;
    
    for (const [property, value] of Object.entries(theme)) {
      root.style.setProperty(property, value);
    }
    
    // Add theme class to body
    document.body.className = document.body.className
      .replace(/theme-\w+/g, '')
      .concat(` theme-${config.value.theme}`);
  }
  
  // Auto-apply theme when it changes
  watch(() => config.value.theme, applyTheme, { immediate: true });
  watch(themeConfig, applyTheme, { deep: true });
  
  // Cleanup
  function destroy() {
    unsubscribe();
  }
  
  return {
    config: computed(() => config.value),
    themeConfig,
    apiConfig,
    uiConfig,
    isLoading: computed(() => isLoading.value),
    errors: computed(() => errors.value),
    
    // Methods
    updateConfig,
    resetConfig,
    getApiKey,
    exportConfig,
    importConfig,
    applyTheme,
    destroy
  };
}
