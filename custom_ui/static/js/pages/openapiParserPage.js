/**
 * OpenAPI Parser Page Controller
 * Manages the OpenAPI JSON Parser tab UI and business logic
 */

function updateJsonParserControls() {
    const input = document.getElementById('jsonFilePrefixInput');
    const checkbox = document.getElementById('jsonDefaultFileNameCheckbox');
    const button = document.getElementById('runJsonParserBtn');
    const clearLink = document.getElementById('jsonClearPrefixLink');
    if (!input || !checkbox || !button || !clearLink) return;

    if (checkbox.checked) {
        input.disabled = true;
        button.disabled = false;
        button.style.background = 'rgba(0, 212, 255, 0.8)';
        button.style.color = '#fff';
        button.style.cursor = 'pointer';
        clearLink.style.opacity = '0.5';
        clearLink.style.pointerEvents = 'none';
    } else if (input.value.trim() !== '') {
        checkbox.disabled = true;
        button.disabled = false;
        button.style.background = 'rgba(0, 212, 255, 0.8)';
        button.style.color = '#fff';
        button.style.cursor = 'pointer';
        clearLink.style.opacity = '1';
        clearLink.style.pointerEvents = 'auto';
    } else {
        checkbox.disabled = false;
        input.disabled = false;
        button.disabled = true;
        button.style.background = 'rgba(0, 212, 255, 0.2)';
        button.style.color = 'rgba(255, 255, 255, 0.4)';
        button.style.cursor = 'not-allowed';
        clearLink.style.opacity = '0.5';
        clearLink.style.pointerEvents = 'none';
    }
}

function clearJsonPrefix() {
    const input = document.getElementById('jsonFilePrefixInput');
    if (input) {
        input.value = '';
        updateJsonParserControls();
    }
}

class OpenAPIParserPage {
    constructor() {
        this.isRunning = false;
        this.init();
    }

    init() {
        console.log('OpenAPIParserPage initialized');
        updateJsonParserControls();
    }

    async runParser() {
        if (this.isRunning) {
            notification.warning('Parser already running');
            return;
        }

        const url = document.getElementById('jsonUrlInput')?.value;
        const checkboxChecked = document.getElementById('jsonDefaultFileNameCheckbox')?.checked;
        const inputValue = document.getElementById('jsonFilePrefixInput')?.value.trim();
        
        console.log('🔍 DEBUG: Checkbox checked:', checkboxChecked);
        console.log('🔍 DEBUG: Input value:', inputValue);
        
        const filenamePrefix = checkboxChecked
            ? 'OpenAPI_Data'
            : (inputValue || 'OpenAPI_Data');
        
        console.log('🔍 DEBUG: Final filename prefix:', filenamePrefix);

        // Validation
        if (!Validators.isNotEmpty(url)) {
            notification.error('Please enter an OpenAPI Spec URL');
            return;
        }

        if (!Validators.isHttpUrl(url)) {
            notification.error('Please enter a valid HTTP/HTTPS URL');
            return;
        }

        // Show loading state
        this.isRunning = true;
        const loadingNotif = notification.info('Running OpenAPI JSON Parser...', 0);
        
        const button = document.getElementById('runJsonParserBtn');
        if (button) {
            button.disabled = true;
            button.textContent = '⏳ Parsing...';
        }

        // Show status
        this.showStatus('⏳', 'Running OpenAPI JSON Parser...');

        try {
            console.log('Running OpenAPI JSON Parser for:', url);
            console.log('Filename prefix:', filenamePrefix);

            const response = await fetch('/run-json-parser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url, filename_prefix: filenamePrefix })
            });

            const data = await response.json();

            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();

            if (data.success) {
                this.displayResults(data);
                notification.success('OpenAPI JSON Parser completed successfully!');
                this.showStatus('✅', 'Parsing completed successfully!');
                console.log('Parser successful:', data);
            } else {
                notification.error(data.error || 'Parsing failed');
                this.showStatus('❌', data.error || 'Parsing failed');
                console.error('Parser failed:', data);
            }
        } catch (error) {
            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();
            
            console.error('Parser error:', error);
            notification.error('Parsing failed: ' + error.message);
            this.showStatus('❌', 'Parsing failed: ' + error.message);
        } finally {
            // Reset state
            this.isRunning = false;
            if (button) {
                updateJsonParserControls();
                button.textContent = '▶️ Run JSON Parser';
            }
        }
    }

    showStatus(icon, text) {
        const statusSection = document.getElementById('statusSection');
        const statusIcon = document.getElementById('statusIcon');
        const statusText = document.getElementById('statusText');
        
        if (statusSection) statusSection.style.display = 'block';
        if (statusIcon) statusIcon.textContent = icon;
        if (statusText) statusText.textContent = text;
    }

    displayResults(data) {
        const resultsSection = document.getElementById('resultsSection');
        const resultsContent = document.getElementById('resultsContent');
        const logsOutput = document.getElementById('logsOutput');
        
        if (resultsSection) resultsSection.style.display = 'block';
        
        if (resultsContent) {
            resultsContent.innerHTML = `
                <h4>📊 Parsing Results:</h4>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 400px;">${JSON.stringify(data.results || data, null, 2)}</pre>
            `;
        }
        
        if (logsOutput && data.logs) {
            logsOutput.textContent = Array.isArray(data.logs) ? data.logs.join('\n') : data.logs;
        }
    }
}

// Create global instance
const openapiParserPage = new OpenAPIParserPage();

// Backward compatibility wrapper
function runJsonParser() {
    openapiParserPage.runParser();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OpenAPIParserPage;
}
