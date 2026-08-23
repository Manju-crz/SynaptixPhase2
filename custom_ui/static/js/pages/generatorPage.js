/**
 * Generator Page Controller
 * Manages the Test Code Generator tab UI and business logic
 */

class GeneratorPage {
    constructor() {
        this.excelFiles = [];
        this.isGenerating = false;
        this.isExecuting = false;
        this.isGeneratingReport = false;
        this.currentTestId = null;
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
        const baseUrlSelect = document.getElementById('generatorBaseUrlSelect');
        if (baseUrlSelect) {
            baseUrlSelect.addEventListener('change', (e) => this.handleBaseUrlChange(e));
        }
    }

    handleBaseUrlChange(event) {
        const customUrlInput = document.getElementById('generatorCustomBaseUrl');
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
                console.log('Excel files loaded for generator:', this.excelFiles.length);
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
        const dropdown = document.getElementById('generatorExcelFileSelect');
        if (!dropdown) {
            console.error('Generator Excel file dropdown not found');
            return;
        }

        dropdown.innerHTML = '<option value="">Select Excel File</option>';
        
        if (this.excelFiles.length === 0) {
            dropdown.innerHTML += '<option value="" disabled>No Excel files found</option>';
            return;
        }

        this.excelFiles.forEach(file => {
            const option = document.createElement('option');
            option.value = file.path;
            option.textContent = file.name;
            dropdown.appendChild(option);
        });

        console.log('Generator Excel dropdown populated with', this.excelFiles.length, 'files');
    }

    async generateTestCode() {
        if (this.isGenerating) {
            notification.warning('Generation already in progress');
            return;
        }

        // Validate inputs
        const excelFile = document.getElementById('generatorExcelFileSelect')?.value;
        const baseUrlSelect = document.getElementById('generatorBaseUrlSelect')?.value;
        const customBaseUrl = document.getElementById('generatorCustomBaseUrl')?.value;
        const folderName = document.getElementById('generatorFolderName')?.value;
        const fileName = document.getElementById('generatorFileName')?.value;
        const query = document.getElementById('generatorQueryInput')?.value;

        // Validation
        if (!Validators.isNotEmpty(excelFile)) {
            notification.error('Please select an Excel file');
            return;
        }

        if (!Validators.isNotEmpty(folderName)) {
            notification.error('Please enter a folder name');
            return;
        }

        if (!Validators.isNotEmpty(fileName)) {
            notification.error('Please enter a file name');
            return;
        }

        if (!Validators.isNotEmpty(query)) {
            notification.error('Please enter a test case prompt');
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
            folder_name: folderName,
            file_name: fileName,
            ai_model: getSelectedAiModel()
        };

        // Show loading state
        this.isGenerating = true;
        const loadingNotif = notification.info('Generating test code...', 0);
        this.showStatus('⏳', 'Generating test code...');
        
        const generateBtn = document.getElementById('runGeneratorBtn');
        if (generateBtn) {
            generateBtn.disabled = true;
            generateBtn.textContent = '⏳ Generating...';
        }

        try {
            console.log('Generating test code with data:', requestData);

            const response = await fetch('/run-generator', {
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
                this.displayGenerationResults(data);
                notification.success('Test code generated successfully!');
                this.showStatus('✅', 'Test code generated successfully!');
                console.log('Generation successful:', data);
            } else {
                notification.error(data.error || 'Generation failed');
                this.showStatus('❌', data.error || 'Generation failed');
                console.error('Generation failed:', data);
            }
        } catch (error) {
            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();
            
            console.error('Generation error:', error);
            notification.error('Generation failed: ' + error.message);
            this.showStatus('❌', 'Generation failed: ' + error.message);
        } finally {
            // Reset state
            this.isGenerating = false;
            if (generateBtn) {
                generateBtn.disabled = false;
                generateBtn.textContent = '⚡ Generate Test Code';
            }
        }
    }

    async executeTest() {
        if (this.isExecuting) {
            notification.warning('Execution already in progress');
            return;
        }

        const folderName = document.getElementById('generatorFolderName')?.value;
        const fileName = document.getElementById('generatorFileName')?.value;

        if (!Validators.isNotEmpty(folderName) || !Validators.isNotEmpty(fileName)) {
            notification.error('Please generate test code first');
            return;
        }

        // Show loading state
        this.isExecuting = true;
        const loadingNotif = notification.info('Executing test...', 0);
        this.showStatus('⏳', 'Executing test...');
        
        const executeBtn = document.getElementById('executeTestBtn');
        if (executeBtn) {
            executeBtn.disabled = true;
            executeBtn.textContent = '⏳ Executing...';
        }

        try {
            const requestData = {
                folder_name: folderName,
                file_name: fileName
            };

            console.log('Executing test with data:', requestData);

            const response = await fetch('/execute-generated-test', {
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
                this.currentTestId = data.test_id;
                this.displayExecutionLogs(data);
                notification.success('Test execution started!');
                this.showStatus('✅', 'Test execution completed!');
                console.log('Execution successful:', data);
            } else {
                notification.error(data.error || 'Execution failed');
                this.showStatus('❌', data.error || 'Execution failed');
                console.error('Execution failed:', data);
            }
        } catch (error) {
            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();
            
            console.error('Execution error:', error);
            notification.error('Execution failed: ' + error.message);
            this.showStatus('❌', 'Execution failed: ' + error.message);
        } finally {
            // Reset state
            this.isExecuting = false;
            if (executeBtn) {
                executeBtn.disabled = false;
                executeBtn.textContent = '▶️ Execute Test';
            }
        }
    }

    async generateReport() {
        if (this.isGeneratingReport) {
            notification.warning('Report generation already in progress');
            return;
        }

        const folderName = document.getElementById('generatorFolderName')?.value;

        if (!Validators.isNotEmpty(folderName)) {
            notification.error('Please execute test first');
            return;
        }

        // Show loading state
        this.isGeneratingReport = true;
        const loadingNotif = notification.info('Generating Allure report...', 0);
        this.showStatus('⏳', 'Generating Allure report...');
        
        const reportBtn = document.getElementById('showReportBtn');
        if (reportBtn) {
            reportBtn.disabled = true;
            reportBtn.textContent = '⏳ Generating...';
        }

        try {
            const requestData = {
                folder_name: folderName
            };

            console.log('Generating report with data:', requestData);

            const response = await fetch('/show-allure-report', {
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
                this.displayReportStatus(data);
                notification.success('Allure report generated!');
                this.showStatus('✅', 'Allure report generated successfully!');
                console.log('Report generation successful:', data);
                
                // Open report in new tab if URL provided
                if (data.report_url) {
                    window.open(data.report_url, '_blank');
                }
            } else {
                notification.error(data.error || 'Report generation failed');
                this.showStatus('❌', data.error || 'Report generation failed');
                console.error('Report generation failed:', data);
            }
        } catch (error) {
            // Remove loading notification
            if (loadingNotif) loadingNotif.remove();
            
            console.error('Report generation error:', error);
            notification.error('Report generation failed: ' + error.message);
            this.showStatus('❌', 'Report generation failed: ' + error.message);
        } finally {
            // Reset state
            this.isGeneratingReport = false;
            if (reportBtn) {
                reportBtn.disabled = false;
                reportBtn.textContent = '📊 Generate Report';
            }
        }
    }

    showStatus(icon, text) {
        const statusSection = document.getElementById('generatorStatus');
        const statusIcon = document.getElementById('generatorStatusIcon');
        const statusText = document.getElementById('generatorStatusText');
        
        if (statusSection) statusSection.style.display = 'block';
        if (statusIcon) statusIcon.textContent = icon;
        if (statusText) statusText.textContent = text;
    }

    hideStatus() {
        const statusSection = document.getElementById('generatorStatus');
        if (statusSection) statusSection.style.display = 'none';
    }

    displayGenerationResults(data) {
        // Show output tabs container
        const outputTabsContainer = document.getElementById('outputTabsContainer');
        if (outputTabsContainer) outputTabsContainer.style.display = 'block';

        // Display results in generation results tab
        const resultsContent = document.getElementById('generationResultsContent');
        if (resultsContent) {
            resultsContent.innerHTML = `
                <h4>📄 Generated Test File:</h4>
                <p><strong>File:</strong> rest_test/${data.folder_name || 'N/A'}/${data.file_name || 'N/A'}.py</p>
                <p><strong>Methods Generated:</strong> ${data.methods_count || 0}</p>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 400px;">${data.generated_code || 'No code generated'}</pre>
            `;
        }

        // Switch to generation results tab
        switchOutputTab('generation-results');
    }

    displayExecutionLogs(data) {
        // Show output tabs container
        const outputTabsContainer = document.getElementById('outputTabsContainer');
        if (outputTabsContainer) outputTabsContainer.style.display = 'block';

        // Display logs in execution logs tab
        const logsContent = document.getElementById('executionLogsContent');
        if (logsContent) {
            logsContent.innerHTML = `
                <h4>🔍 Test Execution Logs:</h4>
                <p><strong>Test ID:</strong> ${data.test_id || 'N/A'}</p>
                <p><strong>Status:</strong> ${data.status || 'Running'}</p>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 400px;">${data.logs || data.output || 'Execution in progress...'}</pre>
            `;
        }

        // Switch to execution logs tab
        switchOutputTab('execution-logs');
    }

    displayReportStatus(data) {
        // Show output tabs container
        const outputTabsContainer = document.getElementById('outputTabsContainer');
        if (outputTabsContainer) outputTabsContainer.style.display = 'block';

        // Display report status
        const reportContent = document.getElementById('reportStatusContent');
        if (reportContent) {
            reportContent.innerHTML = `
                <h4>📊 Allure Report Status:</h4>
                <p><strong>Status:</strong> ${data.status || 'Generated'}</p>
                ${data.report_url ? `<p><strong>Report URL:</strong> <a href="${data.report_url}" target="_blank">${data.report_url}</a></p>` : ''}
                <p>${data.message || 'Report generated successfully'}</p>
                ${data.report_url ? `<button onclick="window.open('${data.report_url}', '_blank')" style="margin-top: 10px; padding: 10px 20px;">🔗 Open Report</button>` : ''}
            `;
        }

        // Switch to report status tab
        switchOutputTab('report-status');
    }

    clearResults() {
        const outputTabsContainer = document.getElementById('outputTabsContainer');
        if (outputTabsContainer) outputTabsContainer.style.display = 'none';
        
        this.hideStatus();
    }
}

// Create global instance
const generatorPage = new GeneratorPage();

// Backward compatibility wrappers
function runGenerator() {
    generatorPage.generateTestCode();
}

function executeGeneratedTest() {
    generatorPage.executeTest();
}

function showAllureReport() {
    generatorPage.generateReport();
}

function reloadGeneratorExcelFiles() {
    generatorPage.loadExcelFiles();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GeneratorPage;
}
