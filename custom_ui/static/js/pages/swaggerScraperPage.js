/**
 * Swagger Scraper Page Controller
 * Manages the Swagger UI Scraper tab UI and business logic
 */

function updateSwaggerScraperControls() {
    const input = document.getElementById('swaggerFilePrefixInput');
    const checkbox = document.getElementById('swaggerDefaultFileNameCheckbox');
    const button = document.getElementById('runUiScraperBtn');
    const clearLink = document.getElementById('swaggerClearPrefixLink');
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

function clearSwaggerPrefix() {
    const input = document.getElementById('swaggerFilePrefixInput');
    if (input) {
        input.value = '';
        updateSwaggerScraperControls();
    }
}

class SwaggerScraperPage {
    constructor() {
        this.isRunning = false;
        this.init();
    }

    init() {
        console.log('SwaggerScraperPage initialized');
        updateSwaggerScraperControls();
    }

    async runScraper() {
        if (this.isRunning) {
            notification.warning('Scraper already running');
            return;
        }

        const url = document.getElementById('uiUrlInput')?.value;
        const checkboxChecked = document.getElementById('swaggerDefaultFileNameCheckbox')?.checked;
        const inputValue = document.getElementById('swaggerFilePrefixInput')?.value.trim();
        
        console.log('🔍 DEBUG: Checkbox checked:', checkboxChecked);
        console.log('🔍 DEBUG: Input value:', inputValue);
        
        const filenamePrefix = checkboxChecked
            ? 'Swagger_Data'
            : (inputValue || 'Swagger_Data');
        
        console.log('🔍 DEBUG: Final filename prefix:', filenamePrefix);

        // Validation
        if (!Validators.isNotEmpty(url)) {
            notification.error('Please enter a Swagger UI URL');
            return;
        }

        if (!Validators.isHttpUrl(url)) {
            notification.error('Please enter a valid HTTP/HTTPS URL');
            return;
        }

        // Show loading state
        this.isRunning = true;
        const loadingNotif = notification.info('Running Swagger UI Scraper... This may take 1-5 minutes', 0);
        
        const button = document.getElementById('runUiScraperBtn');
        if (button) {
            button.disabled = true;
            button.textContent = '⏳ Scraping...';
        }

        // Show status
        this.showStatus('⏳', 'Running Swagger UI Scraper...');

        try {
            console.log('Running Swagger UI Scraper for:', url);
            console.log('Filename prefix:', filenamePrefix);

            const response = await fetch('/run-test', {
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
                notification.success('Swagger UI Scraper completed successfully!');
                this.showStatus('✅', 'Scraping completed successfully!');
                console.log('Scraper successful:', data);
            } else {
                notification.error(data.error || 'Scraping failed');
                this.showStatus('❌', data.error || 'Scraping failed');
                console.error('Scraper failed:', data);
            }
        } catch (error) {
            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();
            
            console.error('Scraper error:', error);
            notification.error('Scraping failed: ' + error.message);
            this.showStatus('❌', 'Scraping failed: ' + error.message);
        } finally {
            // Reset state
            this.isRunning = false;
            if (button) {
                updateSwaggerScraperControls();
                button.textContent = '▶️ Run UI Scraper';
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
                <h4>📊 Scraping Results:</h4>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 400px;">${JSON.stringify(data.results || data, null, 2)}</pre>
            `;
        }
        
        if (logsOutput && data.logs) {
            logsOutput.textContent = Array.isArray(data.logs) ? data.logs.join('\n') : data.logs;
        }
    }
}

// Create global instance
const swaggerScraperPage = new SwaggerScraperPage();

// Backward compatibility wrapper
function runUiScraper() {
    swaggerScraperPage.runScraper();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SwaggerScraperPage;
}
