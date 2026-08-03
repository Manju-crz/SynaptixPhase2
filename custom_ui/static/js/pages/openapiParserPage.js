/**
 * OpenAPI Parser Page Controller
 * Manages the OpenAPI JSON Parser tab UI and business logic
 */

class OpenAPIParserPage {
    constructor() {
        this.isRunning = false;
        this.init();
    }

    init() {
        console.log('OpenAPIParserPage initialized');
    }

    async runParser() {
        if (this.isRunning) {
            notification.warning('Parser already running');
            return;
        }

        const url = document.getElementById('jsonUrlInput')?.value;

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

            const response = await fetch('/run-json-parser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
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
                button.disabled = false;
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
