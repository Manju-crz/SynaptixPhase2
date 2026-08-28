/**
 * Executor Page Controller
 * Manages the Test Executor tab UI and business logic
 */

class ExecutorPage {
    constructor() {
        this.testStructure = [];
        this.selectedTests = new Set();
        this.init();
    }

    init() {
        // Load test structure on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.loadTestStructure();
            });
        } else {
            this.loadTestStructure();
        }
    }

    async loadTestStructure() {
        try {
            const response = await fetch('/get-test-structure');
            const data = await response.json();
            
            if (data.success) {
                this.testStructure = data.structure || [];
                this.renderTestTree();
                console.log('Test structure loaded:', this.testStructure.length, 'folders');
            } else {
                console.error('Failed to load test structure:', data.message);
                this.showError('Failed to load test structure');
            }
        } catch (error) {
            console.error('Error loading test structure:', error);
            this.showError('Error loading test structure: ' + error.message);
        }
    }

    async reloadTestStructure() {
        console.log('🔄 Reloading test structure...');
        
        // Show loading state
        const container = document.getElementById('testTreeContent');
        if (container) {
            container.innerHTML = '<p style="color: #00d4ff; text-align: center;">🔄 Reloading test structure...</p>';
        }

        // Clear current selection
        this.selectedTests.clear();
        this.updateSelectionCount();

        // Reload structure
        await this.loadTestStructure();
        
        console.log('✅ Test structure reloaded successfully');
    }

    renderTestTree() {
        const container = document.getElementById('testTreeContent');
        if (!container) {
            console.error('Test tree container not found');
            return;
        }

        if (this.testStructure.length === 0) {
            container.innerHTML = '<p style="color: #888; text-align: center;">No test files found in rest_test folder</p>';
            return;
        }

        let html = '';

        // Add select all controls
        html += `
            <div class="select-all-controls" style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 10px;">
                    <button onclick="executorPage.selectAll()">✅ Select All</button>
                    <button onclick="executorPage.deselectAll()">❌ Deselect All</button>
                    <button onclick="executorPage.expandAll()">📂 Expand All</button>
                    <button onclick="executorPage.collapseAll()">📁 Collapse All</button>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <a href="javascript:void(0)" onclick="executorPage.clearExecutionResults(event)" 
                       style="color: #ff6b6b; text-decoration: none; font-size: 0.9rem; cursor: pointer; transition: color 0.2s ease;"
                       onmouseover="this.style.color='#ff4444'" onmouseout="this.style.color='#ff6b6b'"
                       title="Clear test execution results">
                        🗑️ Clear Execution Results
                    </a>
                    <button onclick="executorPage.runAllTests()" 
                            style="background: rgba(0, 212, 255, 0.8); color: #fff; font-weight: bold;">
                        ▶️ Run All
                    </button>
                    <button onclick="executorPage.generateAllureReport()" 
                            style="background: rgba(76, 175, 80, 0.8); color: #fff; font-weight: bold;">
                        📊 Generate Report
                    </button>
                </div>
            </div>
        `;

        // Render each folder
        this.testStructure.forEach((folder, folderIndex) => {
            html += this.renderFolder(folder, folderIndex);
        });

        container.innerHTML = html;
    }

    renderFolder(folder, folderIndex) {
        const folderId = `folder-${folderIndex}`;
        
        let html = `
            <div class="tree-folder">
                <div class="tree-folder-header" onclick="executorPage.toggleFolder('${folderId}')">
                    <span class="tree-folder-icon" id="${folderId}-icon" style="margin-right: 12px;">▶</span>
                    <input type="checkbox" 
                           id="${folderId}-checkbox" 
                           class="tree-method-checkbox"
                           onclick="event.stopPropagation(); executorPage.toggleFolderSelection('${folderId}', ${folderIndex})">
                    <span class="tree-folder-name">📁 ${folder.name}</span>
                    <span style="color: #888; font-size: 0.85rem;">(${folder.files.length} files)</span>
                </div>
                <div class="tree-folder-content" id="${folderId}-content">
        `;

        // Render each file in the folder
        folder.files.forEach((file, fileIndex) => {
            html += this.renderFile(file, folderIndex, fileIndex);
        });

        html += `
                </div>
            </div>
        `;

        return html;
    }

    renderFile(file, folderIndex, fileIndex) {
        const fileId = `file-${folderIndex}-${fileIndex}`;
        
        let html = `
            <div class="tree-file">
                <div class="tree-file-header" onclick="executorPage.toggleFile('${fileId}')">
                    <span class="tree-file-icon" id="${fileId}-icon" style="margin-right: 12px;">▶</span>
                    <input type="checkbox" 
                           id="${fileId}-checkbox" 
                           class="tree-method-checkbox"
                           onclick="event.stopPropagation(); executorPage.toggleFileSelection('${fileId}', ${folderIndex}, ${fileIndex})">
                    <span class="tree-file-name">📄 ${file.name}</span>
                    <span style="color: #888; font-size: 0.85rem;">(${file.methods.length} tests)</span>
                </div>
                <div class="tree-file-content" id="${fileId}-content">
        `;

        // Render each method in the file
        file.methods.forEach((method, methodIndex) => {
            html += this.renderMethod(method, folderIndex, fileIndex, methodIndex);
        });

        html += `
                </div>
            </div>
        `;

        return html;
    }

    renderMethod(method, folderIndex, fileIndex, methodIndex) {
        const methodId = `method-${folderIndex}-${fileIndex}-${methodIndex}`;
        const testPath = `${this.testStructure[folderIndex].name}/${this.testStructure[folderIndex].files[fileIndex].name}::${method.name}`;
        
        return `
            <div class="tree-method">
                <input type="checkbox" 
                       id="${methodId}-checkbox" 
                       class="tree-method-checkbox"
                       data-test-path="${testPath}"
                       onchange="executorPage.toggleMethodSelection('${methodId}', '${testPath}')">
                <span class="tree-method-name">🧪 ${method.name}</span>
                ${method.description ? `<span class="tree-method-description">- ${method.description}</span>` : ''}
            </div>
        `;
    }

    toggleFolder(folderId) {
        const content = document.getElementById(`${folderId}-content`);
        const icon = document.getElementById(`${folderId}-icon`);
        
        if (content && icon) {
            content.classList.toggle('expanded');
            icon.classList.toggle('expanded');
            icon.textContent = content.classList.contains('expanded') ? '▼' : '▶';
        }
    }

    toggleFile(fileId) {
        const content = document.getElementById(`${fileId}-content`);
        const icon = document.getElementById(`${fileId}-icon`);
        
        if (content && icon) {
            content.classList.toggle('expanded');
            icon.classList.toggle('expanded');
            icon.textContent = content.classList.contains('expanded') ? '▼' : '▶';
        }
    }

    toggleFolderSelection(folderId, folderIndex) {
        const checkbox = document.getElementById(`${folderId}-checkbox`);
        const isChecked = checkbox.checked;
        
        // Select/deselect all files in this folder
        const folder = this.testStructure[folderIndex];
        folder.files.forEach((file, fileIndex) => {
            const fileCheckbox = document.getElementById(`file-${folderIndex}-${fileIndex}-checkbox`);
            if (fileCheckbox) {
                fileCheckbox.checked = isChecked;
                this.toggleFileSelection(`file-${folderIndex}-${fileIndex}`, folderIndex, fileIndex, isChecked);
            }
        });
    }

    toggleFileSelection(fileId, folderIndex, fileIndex, forceChecked = null) {
        const checkbox = document.getElementById(`${fileId}-checkbox`);
        const isChecked = forceChecked !== null ? forceChecked : checkbox.checked;
        
        // Select/deselect all methods in this file
        const file = this.testStructure[folderIndex].files[fileIndex];
        file.methods.forEach((method, methodIndex) => {
            const methodCheckbox = document.getElementById(`method-${folderIndex}-${fileIndex}-${methodIndex}-checkbox`);
            if (methodCheckbox) {
                methodCheckbox.checked = isChecked;
                const testPath = methodCheckbox.getAttribute('data-test-path');
                if (isChecked) {
                    this.selectedTests.add(testPath);
                } else {
                    this.selectedTests.delete(testPath);
                }
            }
        });

        // Update parent folder checkbox
        this.updateFolderCheckbox(folderIndex);
        this.updateSelectionCount();
    }

    updateFolderCheckbox(folderIndex) {
        // Check if all files in this folder are selected
        const folder = this.testStructure[folderIndex];
        const allFilesSelected = folder.files.every((file, fIndex) => {
            const checkbox = document.getElementById(`file-${folderIndex}-${fIndex}-checkbox`);
            return checkbox && checkbox.checked;
        });
        
        // Update folder checkbox
        const folderCheckbox = document.getElementById(`folder-${folderIndex}-checkbox`);
        if (folderCheckbox) {
            folderCheckbox.checked = allFilesSelected;
        }
    }

    toggleMethodSelection(methodId, testPath) {
        const checkbox = document.getElementById(`${methodId}-checkbox`);
        
        if (checkbox.checked) {
            this.selectedTests.add(testPath);
        } else {
            this.selectedTests.delete(testPath);
        }

        // Update parent file and folder checkboxes
        this.updateParentCheckboxes(methodId);
        this.updateSelectionCount();
    }

    updateParentCheckboxes(methodId) {
        // Extract indices from methodId (format: method-folderIndex-fileIndex-methodIndex)
        const parts = methodId.split('-');
        if (parts.length !== 4) return;
        
        const folderIndex = parseInt(parts[1]);
        const fileIndex = parseInt(parts[2]);
        
        // Check if all methods in this file are selected
        const file = this.testStructure[folderIndex].files[fileIndex];
        const allMethodsSelected = file.methods.every((method, methodIndex) => {
            const checkbox = document.getElementById(`method-${folderIndex}-${fileIndex}-${methodIndex}-checkbox`);
            return checkbox && checkbox.checked;
        });
        
        // Update file checkbox
        const fileCheckbox = document.getElementById(`file-${folderIndex}-${fileIndex}-checkbox`);
        if (fileCheckbox) {
            fileCheckbox.checked = allMethodsSelected;
        }
        
        // Check if all files in this folder are selected
        const folder = this.testStructure[folderIndex];
        const allFilesSelected = folder.files.every((file, fIndex) => {
            const checkbox = document.getElementById(`file-${folderIndex}-${fIndex}-checkbox`);
            return checkbox && checkbox.checked;
        });
        
        // Update folder checkbox
        const folderCheckbox = document.getElementById(`folder-${folderIndex}-checkbox`);
        if (folderCheckbox) {
            folderCheckbox.checked = allFilesSelected;
        }
    }

    selectAll() {
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = true;
            const testPath = checkbox.getAttribute('data-test-path');
            if (testPath) {
                this.selectedTests.add(testPath);
            }
        });
        this.updateSelectionCount();
    }

    deselectAll() {
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        this.selectedTests.clear();
        this.updateSelectionCount();
    }

    expandAll() {
        document.querySelectorAll('.tree-folder-content, .tree-file-content').forEach(content => {
            content.classList.add('expanded');
        });
        document.querySelectorAll('.tree-folder-icon, .tree-file-icon').forEach(icon => {
            icon.classList.add('expanded');
            icon.textContent = '▼';
        });
    }

    collapseAll() {
        document.querySelectorAll('.tree-folder-content, .tree-file-content').forEach(content => {
            content.classList.remove('expanded');
        });
        document.querySelectorAll('.tree-folder-icon, .tree-file-icon').forEach(icon => {
            icon.classList.remove('expanded');
            icon.textContent = '▶';
        });
    }

    updateSelectionCount() {
        const count = this.selectedTests.size;
        console.log('Selected tests:', count);
        
        // Update count display
        const countElement = document.getElementById('selectedTestsCount');
        if (countElement) {
            countElement.textContent = `${count} test${count !== 1 ? 's' : ''} selected`;
        }
        
        // Update run button state
        const runButton = document.getElementById('runTestsBtn');
        if (runButton) {
            if (count > 0) {
                runButton.disabled = false;
                runButton.style.background = 'rgba(0, 212, 255, 0.8)';
                runButton.style.color = '#fff';
                runButton.style.cursor = 'pointer';
            } else {
                runButton.disabled = true;
                runButton.style.background = 'rgba(0, 212, 255, 0.2)';
                runButton.style.color = 'rgba(255, 255, 255, 0.4)';
                runButton.style.cursor = 'not-allowed';
            }
        }
    }

    async runAllTests() {
        console.log('🚀 Running ALL tests using simple default command...');
        console.log('Executing: pytest -v rest_test/');
        
        // Run all tests using the simple default command on the backend
        await this.executeAllTests();
    }

    async runSelectedTests() {
        if (this.selectedTests.size === 0) {
            alert('Please select at least one test to run');
            return;
        }

        const selectedTestsArray = Array.from(this.selectedTests);
        console.log('Running selected tests:', selectedTestsArray);
        
        // Run tests
        await this.executeTests(selectedTestsArray);
    }

    async executeAllTests() {
        // Show progress indicator
        const progressIndicator = document.getElementById('testExecutionProgress');
        if (progressIndicator) {
            progressIndicator.style.display = 'block';
        }

        // Show loading state
        const runButton = document.getElementById('runTestsBtn');
        const originalText = runButton ? runButton.textContent : '';
        if (runButton) {
            runButton.disabled = true;
            runButton.textContent = '⏳ Running all tests...';
            runButton.style.background = 'rgba(0, 212, 255, 0.2)';
            runButton.style.cursor = 'not-allowed';
        }

        // Hide previous results
        const resultsSection = document.getElementById('testResultsSection');
        if (resultsSection) {
            resultsSection.style.display = 'none';
        }

        try {
            const response = await fetch('/run-all-tests', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            const data = await response.json();

            if (data.success) {
                this.displayTestResults(data.results, data.stdout);
                console.log('All tests execution completed:', data.results);
            } else {
                alert('All tests execution failed: ' + (data.message || 'Unknown error'));
                console.error('All tests execution failed:', data);
            }
        } catch (error) {
            console.error('Error running all tests:', error);
            alert('Error running all tests: ' + error.message);
        } finally {
            // Hide progress indicator
            if (progressIndicator) {
                progressIndicator.style.display = 'none';
            }

            // Reset button state
            if (runButton) {
                runButton.disabled = false;
                runButton.textContent = originalText;
                runButton.style.background = 'rgba(0, 212, 255, 0.8)';
                runButton.style.cursor = 'pointer';
            }
        }
    }

    async executeTests(testPaths) {
        console.log('Executing tests:', testPaths);

        // Show progress indicator
        const progressIndicator = document.getElementById('testExecutionProgress');
        if (progressIndicator) {
            progressIndicator.style.display = 'block';
        }

        // Show loading state
        const runButton = document.getElementById('runTestsBtn');
        const originalText = runButton ? runButton.textContent : '';
        if (runButton) {
            runButton.disabled = true;
            runButton.textContent = '⏳ Running tests...';
            runButton.style.background = 'rgba(0, 212, 255, 0.2)';
            runButton.style.cursor = 'not-allowed';
        }

        // Hide previous results
        const resultsSection = document.getElementById('testResultsSection');
        if (resultsSection) {
            resultsSection.style.display = 'none';
        }

        try {
            const response = await fetch('/run-selected-tests', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    test_paths: testPaths
                })
            });

            const data = await response.json();

            if (data.success) {
                this.displayTestResults(data.results, data.stdout);
                console.log('Test execution completed:', data.results);
            } else {
                alert('Test execution failed: ' + (data.message || 'Unknown error'));
                console.error('Test execution failed:', data);
            }
        } catch (error) {
            console.error('Error running tests:', error);
            alert('Error running tests: ' + error.message);
        } finally {
            // Hide progress indicator
            if (progressIndicator) {
                progressIndicator.style.display = 'none';
            }

            // Reset button state
            if (runButton) {
                runButton.disabled = false;
                runButton.textContent = originalText;
                runButton.style.background = 'rgba(0, 212, 255, 0.8)';
                runButton.style.cursor = 'pointer';
            }
        }
    }

    displayTestResults(results, stdout) {
        const resultsSection = document.getElementById('testResultsSection');
        const resultsContent = document.getElementById('testResultsContent');

        if (!resultsSection || !resultsContent) {
            console.error('Results section not found');
            return;
        }

        // Show results section
        resultsSection.style.display = 'block';

        // Build results HTML
        let html = '';

        // Summary
        const totalTests = results.total || 0;
        const passed = results.passed || 0;
        const failed = results.failed || 0;
        const skipped = results.skipped || 0;
        const duration = (results.duration || 0).toFixed(2);

        html += `
            <div style="margin-bottom: 15px; padding: 10px; background: rgba(0, 212, 255, 0.1); border-radius: 5px;">
                <h5 style="margin: 0 0 10px 0; color: #00d4ff;">Summary</h5>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
                    <div>
                        <span style="color: #888;">Total:</span>
                        <span style="color: #fff; font-weight: bold; margin-left: 5px;">${totalTests}</span>
                    </div>
                    <div>
                        <span style="color: #888;">Passed:</span>
                        <span style="color: #00ff00; font-weight: bold; margin-left: 5px;">✅ ${passed}</span>
                    </div>
                    <div>
                        <span style="color: #888;">Failed:</span>
                        <span style="color: #ff6b6b; font-weight: bold; margin-left: 5px;">❌ ${failed}</span>
                    </div>
                    <div>
                        <span style="color: #888;">Skipped:</span>
                        <span style="color: #ffa500; font-weight: bold; margin-left: 5px;">⏭️ ${skipped}</span>
                    </div>
                    <div>
                        <span style="color: #888;">Duration:</span>
                        <span style="color: #fff; font-weight: bold; margin-left: 5px;">⏱️ ${duration}s</span>
                    </div>
                </div>
            </div>
        `;

        // Individual test results
        if (results.tests && results.tests.length > 0) {
            html += '<h5 style="margin: 15px 0 10px 0; color: #00d4ff;">Test Details</h5>';
            
            results.tests.forEach(test => {
                const outcomeIcon = test.outcome === 'passed' ? '✅' : 
                                   test.outcome === 'failed' ? '❌' : 
                                   test.outcome === 'skipped' ? '⏭️' : '❓';
                const outcomeColor = test.outcome === 'passed' ? '#00ff00' : 
                                    test.outcome === 'failed' ? '#ff6b6b' : 
                                    test.outcome === 'skipped' ? '#ffa500' : '#888';
                
                html += `
                    <div style="margin-bottom: 10px; padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px; border-left: 3px solid ${outcomeColor};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.2rem;">${outcomeIcon}</span>
                                <span style="color: #fff; margin-left: 8px;">${test.name}</span>
                            </div>
                            <span style="color: #888; font-size: 0.9rem;">⏱️ ${(test.duration || 0).toFixed(2)}s</span>
                        </div>
                        ${test.message ? `
                            <div style="margin-top: 8px; padding: 8px; background: rgba(0, 0, 0, 0.3); border-radius: 3px; font-family: monospace; font-size: 0.85rem; color: #ff6b6b; white-space: pre-wrap;">
                                ${this.escapeHtml(test.message)}
                            </div>
                        ` : ''}
                    </div>
                `;
            });
        }

        // Show stdout if available
        if (stdout && stdout.trim()) {
            html += `
                <details style="margin-top: 15px;">
                    <summary style="cursor: pointer; color: #00d4ff; font-weight: bold; padding: 5px;">
                        📄 Full Output
                    </summary>
                    <pre style="margin-top: 10px; padding: 10px; background: rgba(0, 0, 0, 0.3); border-radius: 5px; overflow-x: auto; font-size: 0.85rem; color: #ccc; white-space: pre-wrap;">${this.escapeHtml(stdout)}</pre>
                </details>
            `;
        }

        resultsContent.innerHTML = html;

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async clearExecutionResults(event) {
        if (event) event.stopPropagation();

        if (!confirm('Are you sure you want to clear test execution results (allure-results and allure-report folders)?')) {
            return;
        }

        try {
            const response = await fetch('/clear-execution-results', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const result = await response.json();

            if (result.success) {
                alert(result.message || 'Execution results cleared successfully');
                
                // Hide results section
                const resultsSection = document.getElementById('testResultsSection');
                if (resultsSection) {
                    resultsSection.style.display = 'none';
                }
                
                console.log('✅ Execution results cleared');
            } else {
                alert(`Failed to clear results: ${result.message}`);
                console.error('Failed to clear results:', result.message);
            }
        } catch (error) {
            console.error('Error clearing execution results:', error);
            alert(`Error clearing results: ${error.message || 'Please try again.'}`);
        }
    }

    async generateAllureReport() {
        console.log('📊 Generating Allure report...');

        try {
            const response = await fetch('/show-allure-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const result = await response.json();

            if (result.success) {
                alert(result.message || 'Allure report generated successfully');

                if (result.url) {
                    const newWindow = window.open(result.url, '_blank');
                    if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {
                        console.warn('Popup blocked!');
                        alert(`Report generated. Click to open: ${result.url}`);
                    }
                }
                
                console.log('✅ Allure report generated');
            } else {
                alert(`Report generation failed: ${result.message}`);
                console.error('Report generation failed:', result.message);
            }
        } catch (error) {
            console.error('Error generating Allure report:', error);
            alert(`Error generating report: ${error.message || 'Please try again.'}`);
        }
    }

    showError(message) {
        const container = document.getElementById('testTreeContent');
        if (container) {
            container.innerHTML = `<p style="color: #ff6b6b; text-align: center;">❌ ${message}</p>`;
        }
    }

    getSelectedTests() {
        return Array.from(this.selectedTests);
    }
}

// Create global instance
const executorPage = new ExecutorPage();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExecutorPage;
}
