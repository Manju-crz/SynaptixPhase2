/**
 * Executor Page Controller
 * Manages the API Executor tab UI and business logic
 */

class ExecutorPage {
    constructor() {
        this.excelFiles = [];
        this.isExecuting = false;
        this.init();
    }

    init() {
        // Load Excel files on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.loadExcelFiles();
                this.setupEventListeners();
            });
        } else {
            this.loadExcelFiles();
            this.setupEventListeners();
        }
    }

    setupEventListeners() {
        // Base URL select change handler
        const baseUrlSelect = document.getElementById('baseUrlSelect');
        if (baseUrlSelect) {
            baseUrlSelect.addEventListener('change', (e) => this.handleBaseUrlChange(e));
        }
    }

    handleBaseUrlChange(event) {
        const customUrlInput = document.getElementById('customBaseUrl');
        if (customUrlInput) {
            if (event.target.value === 'custom') {
                customUrlInput.style.display = 'block';
                customUrlInput.focus();
            } else {
                customUrlInput.style.display = 'none';
            }
        }
    }

    async loadExcelFiles() {
        try {
            const response = await fetch('/get-excel-files');
            const data = await response.json();
            
            if (data.success) {
                this.excelFiles = data.files || [];
                this.populateExcelDropdown();
                console.log('Excel files loaded:', this.excelFiles.length);
            } else {
                console.error('Failed to load Excel files:', data.error);
                notification.error('Failed to load Excel files');
            }
        } catch (error) {
            console.error('Error loading Excel files:', error);
            notification.error('Error loading Excel files: ' + error.message);
        }
    }

    populateExcelDropdown() {
        const dropdown = document.getElementById('excelFileSelect');
        if (!dropdown) {
            console.error('Excel file dropdown not found');
            return;
        }

        dropdown.innerHTML = '<option value="">Select Excel File</option>';
        
        if (this.excelFiles.length === 0) {
            dropdown.innerHTML += '<option value="" disabled>No Excel files found</option>';
            return;
        }

        this.excelFiles.forEach(file => {
            const option = document.createElement('option');
            option.value = file;
            option.textContent = file;
            dropdown.appendChild(option);
        });

        console.log('Excel dropdown populated with', this.excelFiles.length, 'files');
    }

    async executeQuery() {
        if (this.isExecuting) {
            notification.warning('Execution already in progress');
            return;
        }

        // Validate inputs
        const excelFile = document.getElementById('excelFileSelect')?.value;
        const baseUrlSelect = document.getElementById('baseUrlSelect')?.value;
        const customBaseUrl = document.getElementById('customBaseUrl')?.value;
        const query = document.getElementById('queryInput')?.value;

        // Validation
        if (!Validators.isNotEmpty(excelFile)) {
            notification.error('Please select an Excel file');
            return;
        }

        if (!Validators.isNotEmpty(query)) {
            notification.error('Please enter a query');
            return;
        }

        // Determine base URL
        let baseUrl = baseUrlSelect;
        if (baseUrlSelect === 'custom') {
            if (!Validators.isNotEmpty(customBaseUrl)) {
                notification.error('Please enter a custom base URL');
                return;
            }
            if (!Validators.isHttpUrl(customBaseUrl)) {
                notification.error('Please enter a valid HTTP/HTTPS URL');
                return;
            }
            baseUrl = customBaseUrl;
        }

        // Prepare request data
        const requestData = {
            excel_file: excelFile,
            query: query,
            base_url: baseUrl,
            ai_model: getSelectedAiModel()
        };

        // Show loading state
        this.isExecuting = true;
        const loadingNotif = notification.info('Executing query...', 0);
        const executeBtn = document.getElementById('runExecutorBtn');
        if (executeBtn) {
            executeBtn.disabled = true;
            executeBtn.textContent = '⏳ Executing...';
        }

        try {
            console.log('Executing query with data:', requestData);

            const response = await fetch('/run-executor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();

            if (data.success) {
                this.displayResults(data);
                notification.success('Query executed successfully!');
                console.log('Execution successful:', data);
            } else {
                notification.error(data.error || 'Execution failed');
                console.error('Execution failed:', data);
            }
        } catch (error) {
            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();
            
            console.error('Execution error:', error);
            notification.error('Execution failed: ' + error.message);
        } finally {
            // Reset state
            this.isExecuting = false;
            if (executeBtn) {
                executeBtn.disabled = false;
                executeBtn.textContent = '▶️ Execute Query';
            }
        }
    }

    displayResults(data) {
        // Show results section
        const statusSection = document.getElementById('statusSection');
        const resultsSection = document.getElementById('resultsSection');
        
        if (statusSection) statusSection.style.display = 'block';
        if (resultsSection) resultsSection.style.display = 'block';

        // Display status
        const statusDiv = document.getElementById('status');
        if (statusDiv) {
            statusDiv.innerHTML = `
                <div style="color: #00ff00;">
                    ✅ Execution completed successfully
                </div>
            `;
        }

        // Display results
        const resultsDiv = document.getElementById('results');
        if (resultsDiv) {
            resultsDiv.innerHTML = `
                <h4>📊 Execution Results:</h4>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto;">${JSON.stringify(data, null, 2)}</pre>
            `;
        }

        // Scroll to results
        if (resultsSection) {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    clearResults() {
        const statusSection = document.getElementById('statusSection');
        const resultsSection = document.getElementById('resultsSection');
        
        if (statusSection) statusSection.style.display = 'none';
        if (resultsSection) resultsSection.style.display = 'none';
    }

    getSelectedExcelFile() {
        return document.getElementById('excelFileSelect')?.value || '';
    }

    getSelectedBaseUrl() {
        const baseUrlSelect = document.getElementById('baseUrlSelect')?.value;
        if (baseUrlSelect === 'custom') {
            return document.getElementById('customBaseUrl')?.value || '';
        }
        return baseUrlSelect || '';
    }

    getQuery() {
        return document.getElementById('queryInput')?.value || '';
    }
}

// Create global instance
const executorPage = new ExecutorPage();

// Backward compatibility wrapper
function runExecutor() {
    executorPage.executeQuery();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExecutorPage;
}
