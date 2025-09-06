// utils/ConfigurationManager.js
export class ConfigurationManager {
  constructor() {
    this.config = new Map();
    this.validators = new Map();
    this.observers = new Set();
    this.initializeDefaults();
  }
  
  initializeDefaults() {
    this.setDefaults({
      // API Configuration
      apiProvider: 'hkbu', // hkbu, openrouter, custom
      apiKey: null,
      apiEndpoint: null,
      model: 'gpt-4.1-mini',
      
      // UI Configuration
      theme: 'default', // default, corporate, minimal, dark
      primaryColor: '#6366f1',
      secondaryColor: '#8b5cf6',
      borderRadius: '12px',
      fontFamily: 'system-ui, sans-serif',
      size: 'normal', // compact, normal, expanded
      
      // Behavior Configuration
      systemPrompt: 'You are a helpful AI assistant.',
      welcomeMessage: 'Hello! How can I help you today?',
      enableVoice: true,
      enableTyping: true,
      enableEmail: false,
      autoResize: true,
      
      // Security Configuration
      allowedOrigins: ['*'],
      maxMessageLength: 4000,
      rateLimitMessages: 60, // per minute
      
      // Feature Flags
      features: {
        contextMemory: true,
        tokenTracking: true,
        exportConversation: true,
        customPrompts: false,
        analytics: false
      }
    });
  }
  
  setDefaults(defaults) {
    for (const [key, value] of Object.entries(defaults)) {
      if (!this.config.has(key)) {
        this.config.set(key, value);
      }
    }
  }
  
  // Configuration validation
  addValidator(key, validatorFn) {
    this.validators.set(key, validatorFn);
  }
  
  setupValidators() {
    // API Key validation
    this.addValidator('apiKey', (value) => {
      if (!value) return { valid: false, error: 'API key is required' };
      if (typeof value !== 'string') return { valid: false, error: 'API key must be string' };
      if (value.length < 10) return { valid: false, error: 'API key too short' };
      return { valid: true };
    });
    
    // Theme validation
    this.addValidator('theme', (value) => {
      const validThemes = ['default', 'corporate', 'minimal', 'dark'];
      if (!validThemes.includes(value)) {
        return { valid: false, error: `Theme must be one of: ${validThemes.join(', ')}` };
      }
      return { valid: true };
    });
    
    // Color validation
    this.addValidator('primaryColor', (value) => {
      const colorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
      if (!colorRegex.test(value)) {
        return { valid: false, error: 'Color must be valid hex code' };
      }
      return { valid: true };
    });
    
    // System prompt validation
    this.addValidator('systemPrompt', (value) => {
      if (!value || typeof value !== 'string') {
        return { valid: false, error: 'System prompt must be non-empty string' };
      }
      if (value.length > 2000) {
        return { valid: false, error: 'System prompt too long (max 2000 chars)' };
      }
      return { valid: true };
    });
  }
  
  // Update configuration with validation
  updateConfig(updates, origin = null) {
    const validationErrors = [];
    const validUpdates = {};
    
    for (const [key, value] of Object.entries(updates)) {
      const validator = this.validators.get(key);
      
      if (validator) {
        const validation = validator(value);
        if (!validation.valid) {
          validationErrors.push(`${key}: ${validation.error}`);
          continue;
        }
      }
      
      validUpdates[key] = value;
      this.config.set(key, value);
    }
    
    if (validationErrors.length > 0) {
      throw new Error(`Configuration validation failed:\n${validationErrors.join('\n')}`);
    }
    
    // Notify observers
    this.notifyObservers(validUpdates, origin);
    
    return validUpdates;
  }
  
  // Get configuration value
  get(key, fallback = undefined) {
    return this.config.has(key) ? this.config.get(key) : fallback;
  }
  
  // Get all configuration
  getAll() {
    return Object.fromEntries(this.config);
  }
  
  // Observe configuration changes
  observe(callback) {
    this.observers.add(callback);
    return () => this.observers.delete(callback);
  }
  
  notifyObservers(changes, origin) {
    for (const observer of this.observers) {
      try {
        observer(changes, origin);
      } catch (error) {
        console.error('Configuration observer error:', error);
      }
    }
  }
  
  // Export/Import configuration
  exportConfig() {
    const config = this.getAll();
    // Remove sensitive data
    const sanitized = { ...config };
    if (sanitized.apiKey) {
      sanitized.apiKey = '***REDACTED***';
    }
    return JSON.stringify(sanitized, null, 2);
  }
  
  importConfig(configJson, origin = null) {
    try {
      const config = JSON.parse(configJson);
      return this.updateConfig(config, origin);
    } catch (error) {
      throw new Error(`Invalid configuration JSON: ${error.message}`);
    }
  }
}
