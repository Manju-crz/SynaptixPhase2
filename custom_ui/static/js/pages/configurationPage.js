/**
 * Configuration Page Controller
 * Manages the Configuration tab UI and business logic
 */

class ConfigurationPage {
    constructor() {
        this.modelNames = {
            'openai': 'OpenAI GPT-4o-mini',
            'deepseek': 'DeepSeek v4-coder',
            'groq': 'Groq Llama-3.3-70b'
        };
        this.storageKey = 'synaptix_ai_model';
        this.init();
    }

    init() {
        // Load saved configuration on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.loadConfig());
        } else {
            this.loadConfig();
        }
    }

    /**
     * Save AI model configuration
     */
    saveConfig() {
        const selectElement = document.getElementById('globalAiModelSelect');
        if (!selectElement) {
            console.error('AI Model select element not found');
            return;
        }

        const selectedModel = selectElement.value;

        // Validate selection
        if (!this.modelNames[selectedModel]) {
            notification.error('Invalid AI model selected');
            return;
        }

        // Save to localStorage
        try {
            localStorage.setItem(this.storageKey, selectedModel);
            
            // Update current AI model display
            this.updateModelDisplay(selectedModel);

            // Show success notification (new way)
            notification.success('Configuration saved successfully!');

            // Also show old status div for backward compatibility
            const statusDiv = document.getElementById('modelConfigStatus');
            if (statusDiv) {
                statusDiv.style.display = 'block';
                setTimeout(() => {
                    statusDiv.style.display = 'none';
                }, 3000);
            }

            console.log('AI Model configuration saved:', selectedModel);

            // Dispatch custom event for other components
            window.dispatchEvent(new CustomEvent('aiModelChanged', {
                detail: { model: selectedModel, name: this.modelNames[selectedModel] }
            }));

        } catch (error) {
            console.error('Error saving configuration:', error);
            notification.error('Failed to save configuration');
        }
    }

    /**
     * Load AI model configuration from localStorage
     */
    loadConfig() {
        try {
            const savedModel = localStorage.getItem(this.storageKey) || 'openai';
            
            const selectElement = document.getElementById('globalAiModelSelect');
            if (selectElement) {
                selectElement.value = savedModel;
            }

            this.updateModelDisplay(savedModel);

            console.log('AI Model configuration loaded:', savedModel);
        } catch (error) {
            console.error('Error loading configuration:', error);
            notification.warning('Using default AI model configuration');
        }
    }

    /**
     * Update the current AI model display
     */
    updateModelDisplay(model) {
        const displayElement = document.getElementById('currentAiModel');
        if (displayElement) {
            displayElement.textContent = this.modelNames[model] || this.modelNames['openai'];
        }
    }

    /**
     * Get the currently selected AI model
     */
    getSelectedModel() {
        return localStorage.getItem(this.storageKey) || 'openai';
    }

    /**
     * Get the display name of the currently selected model
     */
    getSelectedModelName() {
        const model = this.getSelectedModel();
        return this.modelNames[model] || this.modelNames['openai'];
    }
}

// Create global instance
const configurationPage = new ConfigurationPage();

// Expose legacy functions for backward compatibility
function saveAiModelConfig() {
    configurationPage.saveConfig();
}

function loadAiModelConfig() {
    configurationPage.loadConfig();
}

function getSelectedAiModel() {
    return configurationPage.getSelectedModel();
}
