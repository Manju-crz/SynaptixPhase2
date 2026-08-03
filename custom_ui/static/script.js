// script.js
// AI Model Configuration Management
function saveAiModelConfig() {
    const selectedModel = document.getElementById('globalAiModelSelect').value;

    // Save to localStorage
    localStorage.setItem('synaptix_ai_model', selectedModel);

    // Update current AI model display
    const modelNames = {
        'openai': 'OpenAI GPT-4o-mini',
        'deepseek': 'DeepSeek v4-coder',
        'groq': 'Groq Llama-3.3-70b'
    };
    document.getElementById('currentAiModel').textContent = modelNames[selectedModel] || 'OpenAI GPT-4o-mini';

    // Show success message
    const statusDiv = document.getElementById('modelConfigStatus');
    statusDiv.style.display = 'block';
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 3000);

    console.log('AI Model configuration saved:', selectedModel);
}

function loadAiModelConfig() {
    const savedModel = localStorage.getItem('synaptix_ai_model') || 'openai';
    document.getElementById('globalAiModelSelect').value = savedModel;

    // Update current AI model display
    const modelNames = {
        'openai': 'OpenAI GPT-4o-mini',
        'deepseek': 'DeepSeek v4-coder',
        'groq': 'Groq Llama-3.3-70b'
    };
    document.getElementById('currentAiModel').textContent = modelNames[savedModel] || 'OpenAI GPT-4o-mini';
}

function getSelectedAiModel() {
    return localStorage.getItem('synaptix_ai_model') || 'openai';
}

// Load AI model config on page load
document.addEventListener('DOMContentLoaded', function() {
    loadAiModelConfig();
});

function switchOutputTab(tabName) {
    // Hide all output tab contents
    const outputContents = document.querySelectorAll('.output-tab-content');
    outputContents.forEach(content => {
        content.style.display = 'none';
        content.classList.remove('active');
    });

    // Remove active class from all output tab buttons
    const outputButtons = document.querySelectorAll('.output-tab-button');
    outputButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Show selected output tab content
    const selectedContent = document.getElementById(tabName);
    if (selectedContent) {
        selectedContent.style.display = 'block';
        selectedContent.classList.add('active');
    }

    // Add active class to corresponding button
    if (tabName === 'generation-results') {
        const genButton = document.querySelector('.output-tab-button:nth-child(1)');
        if (genButton) genButton.classList.add('active');
    } else if (tabName === 'execution-logs') {
        const execButton = document.querySelector('.output-tab-button:nth-child(2)');
        if (execButton) execButton.classList.add('active');
    } else if (tabName === 'report-status') {
        const reportButton = document.querySelector('.output-tab-button:nth-child(3)');
        if (reportButton) reportButton.classList.add('active');
    }
}

function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Activate corresponding button
    event.target.classList.add('active');

    // Hide results when switching tabs
    document.getElementById('statusSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
}

async function runUiScraper() {
    const urlInput = document.getElementById('uiUrlInput');
    const runBtn = document.getElementById('runUiScraperBtn');
    const statusSection = document.getElementById('statusSection');
    const resultsSection = document.getElementById('resultsSection');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');

    const url = urlInput.value.trim();

    if (!url) {
        alert('Please enter a Swagger UI URL');
        return;
    }

    // Show loading state
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Running...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = 'Swagger UI scraping in progress... This may take 1-5 minutes';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/run-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        const result = await response.json();

        // Update status
        statusIcon.className = '';
        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.textContent = 'Swagger UI scraping completed successfully!';
        } else {
            statusSection.className = 'status-section error';
            statusIcon.textContent = '❌';
            statusText.textContent = 'Failed: ' + result.message;
        }

        // Show results
        resultsSection.style.display = 'block';
        const resultsContent = document.getElementById('resultsContent');
        resultsContent.innerHTML = `
            <div class="result-item"><strong>Page Title:</strong> ${result.pageTitle || '-'}</div>
            <div class="result-item"><strong>Page URL:</strong> ${result.pageUrl || '-'}</div>
            <div class="result-item"><strong>Excel File:</strong> ${result.excelFilePath || '-'}</div>
        `;
        document.getElementById('logsOutput').textContent = result.logs ? result.logs.join('\n') : 'No logs available';

    } catch (error) {
        statusSection.className = 'status-section error';
        statusIcon.className = '';
        statusIcon.textContent = '❌';
        statusText.textContent = 'Error: ' + error.message;
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = '▶ Run UI Scraper';
    }
}

async function runJsonParser() {
    const urlInput = document.getElementById('jsonUrlInput');
    const runBtn = document.getElementById('runJsonParserBtn');
    const statusSection = document.getElementById('statusSection');
    const resultsSection = document.getElementById('resultsSection');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');

    const url = urlInput.value.trim();

    if (!url) {
        alert('Please enter an OpenAPI spec URL');
        return;
    }

    // Show loading state
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Running...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = 'Parsing OpenAPI JSON... This should take ~1 second';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/run-json-parser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        const result = await response.json();

        // Update status
        statusIcon.className = '';
        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.textContent = 'OpenAPI JSON parsing completed successfully!';
        } else {
            statusSection.className = 'status-section error';
            statusIcon.textContent = '❌';
            statusText.textContent = 'Failed: ' + result.message;
        }

        // Show results
        resultsSection.style.display = 'block';
        const resultsContent = document.getElementById('resultsContent');
        resultsContent.innerHTML = `
            <div class="result-item"><strong>API Title:</strong> ${result.apiTitle || '-'}</div>
            <div class="result-item"><strong>API Version:</strong> ${result.apiVersion || '-'}</div>
            <div class="result-item"><strong>Operations Extracted:</strong> ${result.operationCount || 0}</div>
            <div class="result-item"><strong>Excel File:</strong> ${result.excelFilePath || '-'}</div>
        `;
        document.getElementById('logsOutput').textContent = result.logs ? result.logs.join('\n') : 'No logs available';

    } catch (error) {
        statusSection.className = 'status-section error';
        statusIcon.className = '';
        statusIcon.textContent = '❌';
        statusText.textContent = 'Error: ' + error.message;
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = '▶ Run JSON Parser';
    }
}

async function loadExcelFiles() {
    const select = document.getElementById('excelFileSelect');

    try {
        console.log('Loading Excel files...');
        select.innerHTML = '<option value="">Loading files...</option>';

        const response = await fetch('/get-excel-files');
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Result:', result);

        select.innerHTML = '';

        if (result.success && result.files && result.files.length > 0) {
            console.log(`Found ${result.files.length} Excel files`);
            result.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file.path;
                option.textContent = `${file.name} (${file.size})`;
                select.appendChild(option);
            });
        } else {
            console.warn('No Excel files found or request failed:', result.message);
            const option = document.createElement('option');
            option.value = '';
            option.textContent = result.message || 'No Excel files found';
            select.appendChild(option);
        }
    } catch (error) {
        console.error('Error loading Excel files:', error);
        select.innerHTML = '<option value="">Error loading files - Check console</option>';
    }
}

async function runExecutor() {
    const excelFileSelect = document.getElementById('excelFileSelect');
    const baseUrlSelect = document.getElementById('baseUrlSelect');
    const customBaseUrlInput = document.getElementById('customBaseUrl');
    const queryInput = document.getElementById('queryInput');
    const runBtn = document.getElementById('runExecutorBtn');
    const statusSection = document.getElementById('statusSection');
    const resultsSection = document.getElementById('resultsSection');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');

    const excelPath = excelFileSelect.value;
    let baseUrl = baseUrlSelect.value;
    const query = queryInput.value.trim();

    // Validation
    if (!excelPath) {
        alert('Please select an Excel file');
        return;
    }

    if (baseUrl === 'custom') {
        baseUrl = customBaseUrlInput.value.trim();
        if (!baseUrl) {
            alert('Please enter a custom base URL');
            return;
        }
    }

    if (!query) {
        alert('Please enter a natural language query');
        return;
    }

    // Show loading state
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Executing...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = 'Executing API call using semantic search...';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/run-executor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                excel_path: excelPath,
                base_url: baseUrl,
                query: query
            })
        });

        const result = await response.json();

        // Update status
        statusIcon.className = '';
        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.textContent = 'API execution completed successfully!';
        } else {
            statusSection.className = 'status-section error';
            statusIcon.textContent = '❌';
            statusText.textContent = 'Failed: ' + result.message;
        }

        // Show results
        resultsSection.style.display = 'block';
        const resultsContent = document.getElementById('resultsContent');

        let resultsHTML = '';

        if (result.results && result.results.length > 0) {
            resultsHTML += `<div class="result-item"><strong>Total Queries:</strong> ${result.results.length}</div>`;
            resultsHTML += `<div class="result-item"><strong>Successful:</strong> ${result.results.filter(r => r.success).length}</div>`;
            resultsHTML += `<div class="result-item"><strong>Failed:</strong> ${result.results.filter(r => !r.success).length}</div>`;

            resultsHTML += '<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">Query Results:</h4>';

            result.results.forEach((r, index) => {
                const statusEmoji = r.success ? '✅' : '❌';

                // Build request details section
                let requestDetailsHTML = '';
                if (r.request_details) {
                    const req = r.request_details;

                    if (req.header_params && Object.keys(req.header_params).length > 0) {
                        requestDetailsHTML += `<div style="margin-top: 10px;"><strong>📋 Request Headers:</strong> <pre style="margin-top: 5px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; font-size: 0.9em;">${JSON.stringify(req.header_params, null, 2)}</pre></div>`;
                    }

                    if (req.query_params && Object.keys(req.query_params).length > 0) {
                        requestDetailsHTML += `<div style="margin-top: 10px;"><strong>🔍 Query Parameters:</strong> <pre style="margin-top: 5px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; font-size: 0.9em;">${JSON.stringify(req.query_params, null, 2)}</pre></div>`;
                    }

                    if (req.path_params && Object.keys(req.path_params).length > 0) {
                        requestDetailsHTML += `<div style="margin-top: 10px;"><strong>🛤️ Path Parameters:</strong> <pre style="margin-top: 5px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; font-size: 0.9em;">${JSON.stringify(req.path_params, null, 2)}</pre></div>`;
                    }

                    if (req.json_payload) {
                        requestDetailsHTML += `<div style="margin-top: 10px;"><strong>📦 Request Body (JSON):</strong> <pre style="margin-top: 5px; background: rgba(0,0,0,0.5); padding: 10px; max-height: 200px; overflow-y: auto; font-size: 0.9em;">${JSON.stringify(req.json_payload, null, 2)}</pre></div>`;
                    }

                    if (req.form_params && Object.keys(req.form_params).length > 0) {
                        requestDetailsHTML += `<div style="margin-top: 10px;"><strong>📝 Form Data:</strong> <pre style="margin-top: 5px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; font-size: 0.9em;">${JSON.stringify(req.form_params, null, 2)}</pre></div>`;
                    }
                }

                resultsHTML += `
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; margin-bottom: 15px; border-radius: 8px; border-left: 3px solid ${r.success ? '#00ff88' : '#ff4757'}">
                        <div><strong>Query ${index + 1}:</strong> ${r.query} ${statusEmoji}</div>
                        ${r.sl_no ? `<div><strong>Sl_No:</strong> ${r.sl_no}</div>` : ''}
                        ${r.method ? `<div><strong>Method:</strong> ${r.method}</div>` : ''}
                        ${r.endpoint ? `<div><strong>Endpoint:</strong> ${r.endpoint}</div>` : ''}
                        ${r.status_code ? `<div><strong>Status Code:</strong> ${r.status_code}</div>` : ''}
                        ${r.response_time ? `<div><strong>Response Time:</strong> ${r.response_time.toFixed(2)}s</div>` : ''}
                        ${r.error ? `<div style="color: #ff4757;"><strong>Error:</strong> ${r.error}</div>` : ''}
                        ${requestDetailsHTML}
                        ${r.response_data ? `<div style="margin-top: 10px;"><strong>📦 Response:</strong> <pre style="margin-top: 5px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; max-height: 200px; overflow-y: auto; font-size: 0.9em;">${JSON.stringify(r.response_data, null, 2)}</pre></div>` : ''}
                    </div>
                `;
            });
        } else {
            resultsHTML = '<div class="result-item">No results available</div>';
        }

        resultsContent.innerHTML = resultsHTML;
        document.getElementById('logsOutput').textContent = result.logs ? result.logs.join('\n') : 'No logs available';

    } catch (error) {
        statusSection.className = 'status-section error';
        statusIcon.className = '';
        statusIcon.textContent = '❌';
        statusText.textContent = 'Error: ' + error.message;
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = '▶ Execute Query';
    }
}

async function runGenerator() {
    const excelFileSelect = document.getElementById('generatorExcelFileSelect');
    const baseUrlSelect = document.getElementById('generatorBaseUrlSelect');
    const customBaseUrlInput = document.getElementById('generatorCustomBaseUrl');
    const folderNameInput = document.getElementById('generatorFolderName');
    const fileNameInput = document.getElementById('generatorFileName');
    const queryInput = document.getElementById('generatorQueryInput');
    const runBtn = document.getElementById('runGeneratorBtn');
    const statusSection = document.getElementById('statusSection');
    const resultsSection = document.getElementById('resultsSection');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');

    const excelPath = excelFileSelect.value;
    let baseUrl = baseUrlSelect.value;
    const folderName = folderNameInput.value.trim();
    const fileName = fileNameInput.value.trim();
    const query = queryInput.value.trim();
    const aiModel = getSelectedAiModel();

    // Validation
    if (!excelPath) {
        alert('Please select an Excel file');
        return;
    }

    if (baseUrl === 'custom') {
        baseUrl = customBaseUrlInput.value.trim();
        if (!baseUrl) {
            alert('Please enter a custom base URL');
            return;
        }
    }

    if (!folderName) {
        alert('Please enter a folder name');
        return;
    }

    if (!fileName) {
        alert('Please enter a test file name');
        return;
    }

    if (!query) {
        alert('Please enter natural language queries');
        return;
    }

    // Show loading state
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Generating...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = 'Generating test script code from test case prompt...';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/run-generator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                excel_path: excelPath,
                base_url: baseUrl,
                folder_name: folderName,
                file_name: fileName,
                query: query,
                ai_model: aiModel
            })
        });

        const result = await response.json();

        // Update status
        statusIcon.className = '';
        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.textContent = 'Test code generated successfully!';

            // Fade out after 3 seconds
            setTimeout(() => {
                statusSection.classList.add('fade-out');
                // Hide completely after fade-out animation completes (1 second)
                setTimeout(() => {
                    statusSection.style.display = 'none';
                    statusSection.classList.remove('fade-out');
                }, 1000);
            }, 3000);
        } else {
            statusSection.className = 'status-section error';
            statusIcon.textContent = '❌';
            statusText.textContent = 'Failed: ' + result.message;
        }

        // Show output tabs container and switch to Generation Results tab
        const outputTabsContainer = document.getElementById('outputTabsContainer');
        console.log('Output tabs container:', outputTabsContainer);
        outputTabsContainer.style.display = 'block';

        // Switch to generation results tab
        switchOutputTab('generation-results');

        const generationResultsContent = document.getElementById('generationResultsContent');
        console.log('Generation results content element:', generationResultsContent);

        let resultsHTML = '';

        if (result.success && result.file_path) {
            resultsHTML += `<div class="result-item"><strong>📄 Generated File:</strong> ${result.file_path}</div>`;
            resultsHTML += `<div class="result-item"><strong>📁 Folder:</strong> ${result.folder_path}</div>`;
            resultsHTML += `<div class="result-item"><strong>🧪 Tests Generated:</strong> ${result.tests_generated}</div>`;

            // Display validation status
            if (result.validation) {
                if (result.validation.success) {
                    resultsHTML += `<div class="result-item" style="color: #00ff88;"><strong>✅ Code Validation:</strong> Passed - No compilation errors</div>`;
                } else {
                    resultsHTML += `<div class="result-item" style="color: #ff4757;"><strong>❌ Code Validation:</strong> Failed - See Execution Logs for details</div>`;
                }
            }

            if (result.tests && result.tests.length > 0) {
                resultsHTML += `<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">Generated Steps:</h4>`;

                result.tests.forEach((test, index) => {
                    resultsHTML += `
                        <div style="background: rgba(0,0,0,0.3); padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 3px solid #00ff88">
                            <div><strong>Step ${index + 1}:</strong> ${test.query}</div>
                            <div><strong>Sl_No:</strong> ${test.sl_no}</div>
                            <div><strong>Method:</strong> ${test.method}</div>
                            <div><strong>Endpoint:</strong> ${test.endpoint}</div>
                        </div>
                    `;
                });
            }

            // Display generated code
            if (result.generated_code && result.generated_code.length > 0) {
                resultsHTML += '<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">📝 Generated Test Code:</h4>';

                // Check if AI-modified method exists
                let hasAiMethod = false;
                result.generated_code.forEach((methodData, index) => {
                    if (methodData.ai_modified) {
                        hasAiMethod = true;
                    }
                    const aiBadge = methodData.ai_modified ? '<span style="margin-left: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold;">🤖 AI-Enhanced</span>' : '';
                    resultsHTML += `
                        <div style="background: rgba(0,0,0,0.3); padding: 15px; margin-bottom: 15px; border-radius: 8px; border-left: 3px solid ${methodData.ai_modified ? '#764ba2' : '#00d4ff'}">
                            <div style="margin-bottom: 10px;">
                                <strong>Method ${index + 1}:</strong> ${methodData.method_name}${aiBadge}
                                <span style="margin-left: 15px; color: #00ff88;">Lines: ${methodData.line_count}</span>
                                <span style="margin-left: 15px; color: #ffa500;">Steps: ${methodData.step_count}</span>
                            </div>
                            <pre style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 400px; overflow-y: auto; font-size: 0.85em; line-height: 1.4; color: #e0e0e0;"><code class="language-python">${escapeHtml(methodData.code)}</code></pre>
                        </div>
                    `;
                });
            }

            resultsHTML += '<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">How to Run:</h4>';
            resultsHTML += `<div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">`;
            resultsHTML += `<div style="margin-bottom: 10px;"><strong>Run tests:</strong></div>`;
            resultsHTML += `<pre style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; font-size: 0.9em;">pytest ${result.file_path} -v</pre>`;
            resultsHTML += `<div style="margin-top: 15px; margin-bottom: 10px;"><strong>Run with Allure:</strong></div>`;
            resultsHTML += `<pre style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; font-size: 0.9em;">pytest ${result.file_path} --alluredir=allure-results -v</pre>`;
            resultsHTML += `</div>`;
        } else {
            resultsHTML = `<div class="result-item" style="color: #ff4757;">${result.message || 'No results available'}</div>`;
        }

        console.log('Setting results HTML, length:', resultsHTML.length);
        generationResultsContent.innerHTML = resultsHTML;
        console.log('Results HTML set successfully');

        // Display logs in Execution Logs tab (including validation logs)
        const executionLogsContent = document.getElementById('executionLogsContent');
        if (executionLogsContent && result.logs && result.logs.length > 0) {
            let logsHTML = '<div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">';
            logsHTML += '<h4 style="color: #00d4ff; margin-top: 0;">📋 Generation & Validation Logs</h4>';
            logsHTML += '<pre style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 0.9em; line-height: 1.6; color: #e0e0e0; white-space: pre-wrap;">';
            logsHTML += result.logs.join('\n');
            logsHTML += '</pre></div>';
            executionLogsContent.innerHTML = logsHTML;
            console.log('Execution logs displayed, count:', result.logs.length);
        } else {
            console.log('Execution logs element not found or no logs in result');
        }

        // Also display in old logsOutput if it exists (for backward compatibility)
        const logsOutput = document.getElementById('logsOutput');
        if (logsOutput && result.logs) {
            logsOutput.textContent = result.logs.join('\n');
        }

    } catch (error) {
        statusSection.className = 'status-section error';
        statusIcon.className = '';
        statusIcon.textContent = '❌';
        statusText.textContent = 'Error: ' + error.message;
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = '⚡ Generate Test Code';
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Allow Enter key to trigger appropriate test
document.addEventListener('DOMContentLoaded', function() {
    // Load Excel files when page loads
    loadExcelFiles();

    // Also load files for Generator tab
    setTimeout(() => {
        const generatorSelect = document.getElementById('generatorExcelFileSelect');
        if (generatorSelect) {
            loadExcelFilesForGenerator();
        }
    }, 100);

    // Handle base URL selection for Executor
    document.getElementById('baseUrlSelect').addEventListener('change', function(e) {
        const customUrlInput = document.getElementById('customBaseUrl');
        if (e.target.value === 'custom') {
            customUrlInput.style.display = 'block';
        } else {
            customUrlInput.style.display = 'none';
        }
    });

    // Handle base URL selection for Generator
    document.getElementById('generatorBaseUrlSelect').addEventListener('change', function(e) {
        const customUrlInput = document.getElementById('generatorCustomBaseUrl');
        if (e.target.value === 'custom') {
            customUrlInput.style.display = 'block';
        } else {
            customUrlInput.style.display = 'none';
        }
    });

    document.getElementById('uiUrlInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            runUiScraper();
        }
    });

    document.getElementById('jsonUrlInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            runJsonParser();
        }
    });
});

async function loadExcelFilesForGenerator() {
    const select = document.getElementById('generatorExcelFileSelect');

    try {
        console.log('Loading Excel files for Generator...');
        select.innerHTML = '<option value="">Loading files...</option>';

        const response = await fetch('/get-excel-files');
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Result:', result);

        select.innerHTML = '';

        if (result.success && result.files && result.files.length > 0) {
            console.log(`Found ${result.files.length} Excel files for Generator`);
            result.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file.path;
                option.textContent = `${file.name} (${file.size})`;
                select.appendChild(option);
            });
        } else {
            console.warn('No Excel files found or request failed:', result.message);
            const option = document.createElement('option');
            option.value = '';
            option.textContent = result.message || 'No Excel files found';
            select.appendChild(option);
        }
    } catch (error) {
        console.error('Error loading Excel files for Generator:', error);
        select.innerHTML = '<option value="">Error loading files - Check console</option>';
    }
}

async function executeGeneratedTest() {
    const executeBtn = document.getElementById('executeTestBtn');
    const statusSection = document.getElementById('generatorStatus');
    const statusIcon = document.getElementById('generatorStatusIcon');
    const statusText = document.getElementById('generatorStatusText');

    // Get folder and file names from UI input fields
    const folderNameInput = document.getElementById('generatorFolderName');
    const fileNameInput = document.getElementById('generatorFileName');

    const folderName = folderNameInput.value.trim();
    const fileName = fileNameInput.value.trim();

    // Validation
    if (!folderName) {
        alert('Please enter a folder name');
        return;
    }

    if (!fileName) {
        alert('Please enter a test file name');
        return;
    }

    // Show loading state
    executeBtn.disabled = true;
    executeBtn.textContent = '⏳ Executing...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = 'Executing test...';

    try {
        console.log('Starting test execution...');

        // Start test execution
        const response = await fetch('/execute-generated-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                folder_name: folderName,
                file_name: fileName
            })
        });

        const startResult = await response.json();
        console.log('Start result:', startResult);

        if (!startResult.success || !startResult.test_id) {
            throw new Error(startResult.message || 'Failed to start test execution');
        }

        // Poll for results
        const testId = startResult.test_id;
        console.log('Test ID:', testId, '- Starting to poll...');

        let result = null;
        let pollCount = 0;
        const maxPolls = 120; // 2 minutes max (120 * 1 second)

        while (pollCount < maxPolls) {
            await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
            pollCount++;

            console.log(`Polling attempt ${pollCount}/${maxPolls}...`);

            const statusResponse = await fetch(`/check-test-status/${testId}`);
            const statusResult = await statusResponse.json();

            console.log('Status result:', statusResult);

            if (statusResult.status === 'completed') {
                result = statusResult;
                console.log('Test completed! Result:', result);
                break;
            }
        }

        if (!result) {
            console.error('Test execution timed out after', maxPolls, 'polls');
            throw new Error('Test execution timed out');
        }

        // Update status
        statusIcon.className = '';
        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.innerHTML = `Test executed successfully!<br><code style="font-size: 0.85em; color: #00ff88;">Exit Code: ${result.exit_code}</code>`;

            // Fade out after 3 seconds
            setTimeout(() => {
                statusSection.classList.add('fade-out');
                // Hide completely after fade-out animation completes (1 second)
                setTimeout(() => {
                    statusSection.style.display = 'none';
                    statusSection.classList.remove('fade-out');
                }, 1000);
            }, 3000);

            // Show output tabs container and switch to Execution Logs tab
            const outputTabsContainer = document.getElementById('outputTabsContainer');
            outputTabsContainer.style.display = 'block';

            // Switch to execution logs tab
            const executionTab = document.querySelector('.output-tab-button:nth-child(2)');
            if (executionTab) executionTab.click();

            // Show test output in execution logs
            const executionLogsContent = document.getElementById('executionLogsContent');
            let logHTML = '<div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">';
            logHTML += '<h4 style="color: #00d4ff; margin-bottom: 15px;">🧪 Test Execution Details</h4>';
            logHTML += '<div class="result-item"><strong>Command:</strong> <code style="color: #00ff88;">' + result.command + '</code></div>';
            logHTML += '<div class="result-item"><strong>Exit Code:</strong> <code style="color: #00ff88;">' + result.exit_code + '</code></div>';
            
            // Combine stdout and stderr for complete output (pytest logs go to stderr)
            let combinedOutput = '';
            if (result.stderr && result.stderr.trim()) {
                combinedOutput = result.stderr;
            }
            if (result.stdout && result.stdout.trim()) {
                combinedOutput += (combinedOutput ? '\n\n' : '') + result.stdout;
            }
            
            if (combinedOutput) {
                logHTML += '<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">📋 Test Execution Logs:</h4>';
                logHTML += '<pre style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; color: #e0e0e0; overflow-x: auto; white-space: pre-wrap; font-family: \'Consolas\', \'Monaco\', monospace; font-size: 0.9em; line-height: 1.5;">' + combinedOutput + '</pre>';
            } else {
                logHTML += '<p style="color: #a0a0a0; margin-top: 20px;">No output captured.</p>';
            }
            
            logHTML += '</div>';
            executionLogsContent.innerHTML = logHTML;
        } else {
            statusSection.className = 'status-section error';
            statusIcon.textContent = '❌';
            statusText.textContent = 'Test execution failed: ' + result.message;

            // Show output tabs container and switch to Execution Logs tab
            const outputTabsContainer = document.getElementById('outputTabsContainer');
            outputTabsContainer.style.display = 'block';

            // Switch to execution logs tab
            const executionTab = document.querySelector('.output-tab-button:nth-child(2)');
            if (executionTab) executionTab.click();

            // Show error in execution logs
            const executionLogsContent = document.getElementById('executionLogsContent');
            let errorHTML = '<div style="background: rgba(255,71,87,0.1); padding: 15px; border-radius: 8px;">';
            errorHTML += '<h4 style="color: #ff4757; margin-bottom: 15px;">❌ Test Execution Failed</h4>';
            errorHTML += '<div class="result-item"><strong>Message:</strong> ' + result.message + '</div>';
            if (result.command) {
                errorHTML += '<div class="result-item"><strong>Command:</strong> <code style="color: #ff4757;">' + result.command + '</code></div>';
            }
            if (result.stdout) {
                errorHTML += '<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">STDOUT:</h4>';
                errorHTML += '<pre style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; color: #ccc; overflow-x: auto; white-space: pre-wrap;">' + result.stdout + '</pre>';
            }
            if (result.stderr) {
                errorHTML += '<h4 style="color: #ff4757; margin-top: 20px; margin-bottom: 10px;">STDERR:</h4>';
                errorHTML += '<pre style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; color: #ff4757; overflow-x: auto; white-space: pre-wrap;">' + result.stderr + '</pre>';
            }
            if (result.error) {
                errorHTML += '<h4 style="color: #ff4757; margin-top: 20px; margin-bottom: 10px;">ERROR:</h4>';
                errorHTML += '<pre style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; color: #ff4757; overflow-x: auto; white-space: pre-wrap;">' + result.error + '</pre>';
            }
            errorHTML += '</div>';
            executionLogsContent.innerHTML = errorHTML;
        }

    } catch (error) {
        statusSection.className = 'status-section error';
        statusIcon.textContent = '❌';
        statusIcon.className = '';
        statusText.textContent = 'Failed to execute test: ' + error.message;
    } finally {
        executeBtn.disabled = false;
        executeBtn.textContent = '▶ Execute Test';
    }
}

async function showAllureReport() {
    const reportBtn = document.getElementById('showReportBtn');
    const statusSection = document.getElementById('generatorStatus');
    const statusIcon = document.getElementById('generatorStatusIcon');
    const statusText = document.getElementById('generatorStatusText');

    console.log('Opening Allure report...');

    // Show loading state
    reportBtn.disabled = true;
    reportBtn.textContent = '⏳ Opening...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = 'Starting Allure server...';

    try {
        const response = await fetch('/show-allure-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        console.log('Allure report result:', result);

        statusIcon.className = '';

        // Show output tabs container and switch to Report Status tab
        const outputTabsContainer = document.getElementById('outputTabsContainer');
        outputTabsContainer.style.display = 'block';
        switchOutputTab('report-status');

        const reportStatusContent = document.getElementById('reportStatusContent');

        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.textContent = 'Report generated successfully!';

            // Display in Report Status tab
            let reportHTML = '<div style="background: rgba(0,255,136,0.1); padding: 20px; border-radius: 8px; border: 1px solid #00ff88;">';
            reportHTML += '<h4 style="color: #00ff88; margin-bottom: 15px;">✅ Report Generated Successfully</h4>';
            reportHTML += '<div class="result-item"><strong>Message:</strong> ' + (result.message || 'Allure report generated successfully') + '</div>';

            // Open report in new tab of same browser
            if (result.url) {
                console.log('Opening report at:', result.url);
                const newWindow = window.open(result.url, '_blank');

                // Check if popup was blocked
                if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {
                    console.warn('Popup blocked! Showing clickable link instead.');
                    reportHTML += '<div style="margin-top: 20px; padding: 15px; background: rgba(0,212,255,0.1); border-radius: 8px; border: 1px solid #00d4ff;">';
                    reportHTML += '<p style="color: #00d4ff; margin-bottom: 10px;">🔗 <strong>Report Ready!</strong></p>';
                    reportHTML += '<p style="color: #ccc; margin-bottom: 15px;">Click the link below to open the Allure report:</p>';
                    reportHTML += '<a href="' + result.url + '" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(90deg, #00d4ff, #7b2cbf); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">🔗 Open Allure Report</a>';
                    reportHTML += '</div>';
                } else {
                    console.log('Report opened successfully in new tab');
                    reportHTML += '<div style="margin-top: 15px; color: #00ff88;"><strong>✓</strong> Report opened in new browser tab</div>';
                }
            }
            reportHTML += '</div>';
            reportStatusContent.innerHTML = reportHTML;

            // Fade out status message after 3 seconds
            setTimeout(() => {
                statusSection.classList.add('fade-out');
                setTimeout(() => {
                    statusSection.style.display = 'none';
                    statusSection.classList.remove('fade-out');
                }, 1000);
            }, 3000);
        } else {
            statusSection.className = 'status-section error';
            statusIcon.textContent = '❌';
            statusText.textContent = result.message || 'Failed to open Allure report';

            // Display error in Report Status tab
            let errorHTML = '<div style="background: rgba(255,71,87,0.1); padding: 20px; border-radius: 8px; border: 1px solid #ff4757;">';
            errorHTML += '<h4 style="color: #ff4757; margin-bottom: 15px;">❌ Report Generation Failed</h4>';
            errorHTML += '<div class="result-item"><strong>Message:</strong> ' + (result.message || 'Failed to generate Allure report') + '</div>';
            errorHTML += '</div>';
            reportStatusContent.innerHTML = errorHTML;
        }

    } catch (error) {
        console.error('Error opening Allure report:', error);
        statusSection.className = 'status-section error';
        statusIcon.textContent = '❌';
        statusIcon.className = '';
        statusText.textContent = 'Failed to open Allure report: ' + error.message;
    } finally {
        reportBtn.disabled = false;
        reportBtn.textContent = '📊 Generate Report';
    }
}
