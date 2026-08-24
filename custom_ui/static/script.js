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

function switchOutputTab(tabName, compNum, classNum, subNum) {
    // Scope to the specific sub-section if all of compNum, classNum and subNum are provided;
    // otherwise fall back to test class section, then component panel.
    let scope = document;
    if (compNum && classNum && subNum) {
        const subSection = document.getElementById(`subSection_${compNum}_${classNum}_${subNum}`);
        if (subSection) scope = subSection;
    } else if (compNum && classNum) {
        const section = document.getElementById(`testClass_${compNum}_${classNum}`);
        if (section) scope = section;
    } else if (compNum) {
        const panel = document.getElementById(`tcPanel_${compNum}`);
        if (panel) scope = panel;
    }

    // Hide all output tab contents within scope
    const outputContents = scope.querySelectorAll('.output-tab-content');
    outputContents.forEach(content => {
        content.style.display = 'none';
        content.classList.remove('active');
    });

    // Remove active class from all output tab buttons within scope
    const outputButtons = scope.querySelectorAll('.output-tab-button');
    outputButtons.forEach(button => {
        button.classList.remove('active');
        button.style.borderBottomColor = 'transparent';
        button.style.color = '#a0a0a0';
    });

    // Show selected output tab content
    const selectedContent = document.getElementById(tabName);
    if (selectedContent) {
        selectedContent.style.display = 'block';
        selectedContent.classList.add('active');
    }

    // Add active class to the clicked button (find by data-output attribute)
    const activeBtn = scope.querySelector(`.output-tab-button[data-output="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.style.borderBottomColor = '#00d4ff';
        activeBtn.style.color = '#00d4ff';
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

function toggleCollapsibleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (!section) return;
    section.classList.toggle('collapsed');
}

// ===== TestComponent sub-tab management =====
let testComponentCounter = 0;
let activeTestComponent = 1;

// Per-component test class counters
let testClassCounters = {};

// Per-test-class sub-section counters (keyed by `${compNum}_${classNum}`)
let subSectionCounters = {};

function deriveClassName(folderName, fileName) {
    const raw = `${folderName || ''}${fileName || ''}`;
    let name = raw.replace(/[^A-Za-z0-9]/g, '');
    if (!name || !/^[A-Za-z]/.test(name)) {
        name = `Test${name}`;
    }
    return name;
}

function updateComponentClassNames(num) {
    const folderInput = document.getElementById(`generatorFolderName_${num}`);
    const folderName = (folderInput ? folderInput.value.trim() : '') || `TestComponent_${String(num).padStart(2, '0')}`;
    const container = document.getElementById(`testClassesContainer_${num}`);
    if (!container) return;

    const classSections = container.querySelectorAll('.test-class-section');
    classSections.forEach(section => {
        const id = section.id.replace('testClass_', '');
        const fileName = section.getAttribute('data-file-name');
        if (!fileName) return;
        const className = deriveClassName(folderName, fileName);
        section.setAttribute('data-class-name', className);
        updateTestClassTitle(id);
    });
}

function createTestClassHTML(compNum, classNum) {
    const id = `${compNum}_${classNum}`;
    const fileName = `TestFile_${String(classNum).padStart(2, '0')}`;
    const folderInput = document.getElementById(`generatorFolderName_${compNum}`);
    const folderName = (folderInput ? folderInput.value.trim() : '') || `TestComponent_${String(compNum).padStart(2, '0')}`;
    const defaultClassName = deriveClassName(folderName, fileName);
    const closeBtn = `<button class="tc-class-close" onclick="removeTestClass(${compNum}, ${classNum}, event)" title="Remove Test Class">&times;</button>`;
    return `
        <div class="test-class-section" id="testClass_${id}" data-file-name="${fileName}" data-class-name="${defaultClassName}">
            <div class="test-class-header" onclick="toggleTestClassBody('${id}')">
                <span class="test-class-toggle">▼</span>
                <span class="test-class-title" id="testClassTitle_${id}">📘 ${fileName}::${defaultClassName}</span>
                <a href="javascript:void(0)" class="tc-class-rename-link" onclick="showRenameTestClassNameInput('${id}', event)" title="Rename Test Class">Rename Class</a>
                <a href="javascript:void(0)" class="tc-class-rename-link" onclick="showRenameTestClassInput('${id}', event)" title="Rename Test File">Rename Test File</a>
                <a href="javascript:void(0)" class="tc-class-delete-link" onclick="deleteTestFile('${id}', event)" title="Delete Test File">Delete File</a>
                <button class="tc-class-execute-btn" id="tcExecuteBtn_${id}" onclick="executeClassTests(${compNum}, ${classNum}, event)" title="Execute all tests in this class" type="button">▶ Execute Tests</button>
                <div class="tc-class-rename-editor" id="testClassRenameEditor_${id}" style="display: none;">
                    <input type="text" id="testClassRenameInput_${id}" placeholder="Enter new file name" class="tc-class-rename-input">
                    <button class="tc-class-rename-save" onclick="saveTestClassName('${id}', event)" title="Save">✓</button>
                    <button class="tc-class-rename-cancel" onclick="cancelRenameTestClass('${id}', event)" title="Cancel">✕</button>
                </div>
                <div class="tc-class-rename-editor" id="testClassClassRenameEditor_${id}" style="display: none;">
                    <input type="text" id="testClassClassRenameInput_${id}" placeholder="Enter new class name" class="tc-class-rename-input">
                    <button class="tc-class-rename-save" onclick="saveTestClassClassName('${id}', event)" title="Save">✓</button>
                    <button class="tc-class-rename-cancel" onclick="cancelRenameTestClassName('${id}', event)" title="Cancel">✕</button>
                </div>
                ${closeBtn}
            </div>
            <div class="test-class-body" id="testClassBody_${id}">
                <div class="sub-sections-container" id="subSectionsContainer_${id}">
                    <button class="sub-section-add-btn" onclick="addSubSection(${compNum}, ${classNum})" title="Add new Test Method">+ Add Test Method</button>
                </div>
                <div class="class-execution-logs" id="classExecutionLogs_${id}" style="display: none; margin-top: 15px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 8px; border-left: 3px solid #00d4ff;"></div>
            </div>
        </div>
    `;
}

function createSubSectionHTML(compNum, classNum, subNum) {
    const id = `${compNum}_${classNum}`;
    const subId = `${id}_${subNum}`;
    const closeBtn = `<button class="sub-section-close" onclick="removeSubSection(${compNum}, ${classNum}, ${subNum}, event)" title="Remove Sub Section">&times;</button>`;
    return `
        <div class="sub-section" id="subSection_${subId}">
            <div class="sub-section-header" onclick="toggleSubSectionBody('${id}', ${subNum})">
                <span class="sub-section-toggle">▼</span>
                <span class="sub-section-title" id="subSectionTitle_${subId}">📝 TestMethod_${String(subNum).padStart(2, '0')}</span>
                <a href="javascript:void(0)" class="sub-section-delete-link sub-section-delete-disabled" id="subSectionDeleteLink_${subId}" onclick="deleteTestMethod('${id}', ${subNum}, event)" title="Generate test code first to enable">Delete Method</a>
                <a href="javascript:void(0)" class="sub-section-rename-link sub-section-rename-disabled" id="subSectionRenameLink_${subId}" onclick="showRenameSubSectionInput('${id}', ${subNum}, event)" title="Generate test code first to enable">Append Method Name</a>
                <div class="sub-section-rename-editor" id="subSectionRenameEditor_${subId}" style="display: none;">
                    <input type="text" id="subSectionRenameInput_${subId}" placeholder="Enter new name" class="sub-section-rename-input">
                    <button class="sub-section-rename-save" onclick="saveSubSectionName('${id}', ${subNum}, event)" title="Save">✓</button>
                    <button class="sub-section-rename-cancel" onclick="cancelRenameSubSection('${id}', ${subNum}, event)" title="Cancel">✕</button>
                </div>
                ${closeBtn}
            </div>
            <div class="sub-section-body" id="subSectionBody_${subId}">
                <label for="generatorQueryInput_${subId}">💬 Natural Language Test case Prompt:</label>
                <textarea
                    id="generatorQueryInput_${subId}"
                    placeholder="Example: Create a new pet in the pet store&#10;Multiple queries: Create a new pet; Update pet information; Delete a pet&#10;&#10;Note: Each query will generate a separate test method"
                    rows="4"
                    class="textarea-input"
                    onchange="updatePromptSidecar(${compNum}, ${classNum}, ${subNum})"
                ></textarea>

                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
                    <button class="sub-section-action-btn" id="runGeneratorBtn_${subId}" onclick="runGenerator(${compNum}, ${classNum}, ${subNum})" style="flex: 1; min-width: 150px; padding: 10px 15px; font-size: 0.9em;">
                        ⚡ Generate Test Code
                    </button>

                    <button class="sub-section-action-btn" id="executeTestBtn_${subId}" onclick="executeGeneratedTest(${compNum}, ${classNum}, ${subNum})" style="flex: 1; min-width: 150px; padding: 10px 15px; font-size: 0.9em;">
                        ▶️ Execute Test
                    </button>

                    <button class="sub-section-action-btn" id="showReportBtn_${subId}" onclick="showAllureReport(${compNum}, ${classNum}, ${subNum})" style="flex: 1; min-width: 150px; padding: 10px 15px; font-size: 0.9em;">
                        📊 Generate Report
                    </button>
                </div>

                <div id="generatorStatus_${subId}" class="status-section" style="display: none; margin-top: 15px;">
                    <span id="generatorStatusIcon_${subId}">⏳</span>
                    <span id="generatorStatusText_${subId}">Processing...</span>
                </div>

                <!-- Output Tabs -->
                <div id="outputTabsContainer_${subId}" style="display: none; margin-top: 20px;">
                    <div style="display: flex; gap: 10px; border-bottom: 2px solid rgba(255, 255, 255, 0.1); margin-bottom: 15px;">
                        <button class="output-tab-button active" data-comp="${compNum}" data-class="${classNum}" data-sub="${subNum}" data-output="generation-results_${subId}" onclick="switchOutputTab('generation-results_${subId}', ${compNum}, ${classNum}, ${subNum})" style="padding: 10px 20px; font-size: 0.9em; border: none; background: transparent; color: #a0a0a0; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.3s;">
                            📄 Generation Results
                        </button>
                        <button class="output-tab-button" data-comp="${compNum}" data-class="${classNum}" data-sub="${subNum}" data-output="execution-logs_${subId}" onclick="switchOutputTab('execution-logs_${subId}', ${compNum}, ${classNum}, ${subNum})" style="padding: 10px 20px; font-size: 0.9em; border: none; background: transparent; color: #a0a0a0; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.3s;">
                            🔍 Execution Logs
                        </button>
                        <button class="output-tab-button" data-comp="${compNum}" data-class="${classNum}" data-sub="${subNum}" data-output="report-status_${subId}" onclick="switchOutputTab('report-status_${subId}', ${compNum}, ${classNum}, ${subNum})" style="padding: 10px 20px; font-size: 0.9em; border: none; background: transparent; color: #a0a0a0; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.3s;">
                            📊 Report Status
                        </button>
                    </div>

                    <div id="generation-results_${subId}" class="output-tab-content active" style="display: block;">
                        <div id="generationResultsContent_${subId}"></div>
                    </div>

                    <div id="execution-logs_${subId}" class="output-tab-content" style="display: none;">
                        <div id="executionLogsContent_${subId}"></div>
                    </div>

                    <div id="report-status_${subId}" class="output-tab-content" style="display: none;">
                        <div id="reportStatusContent_${subId}"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function addSubSection(compNum, classNum) {
    const id = `${compNum}_${classNum}`;
    if (!subSectionCounters[id]) subSectionCounters[id] = 0;
    subSectionCounters[id]++;
    const subNum = subSectionCounters[id];

    const container = document.getElementById(`subSectionsContainer_${id}`);
    if (!container) return;

    // Insert new sub-section before the add button
    const addBtn = container.querySelector('.sub-section-add-btn');
    const html = createSubSectionHTML(compNum, classNum, subNum);
    addBtn.insertAdjacentHTML('beforebegin', html);
}

function removeSubSection(compNum, classNum, subNum, event) {
    if (event) event.stopPropagation();
    const id = `${compNum}_${classNum}`;
    const container = document.getElementById(`subSectionsContainer_${id}`);
    if (!container) return;
    const sections = container.querySelectorAll('.sub-section');
    if (sections.length <= 1) return; // Don't remove the last one

    const section = document.getElementById(`subSection_${id}_${subNum}`);
    if (section) section.remove();
}

function toggleSubSectionBody(id, subNum) {
    const subId = `${id}_${subNum}`;
    const body = document.getElementById(`subSectionBody_${subId}`);
    const section = document.getElementById(`subSection_${subId}`);
    if (!body || !section) return;
    section.classList.toggle('collapsed');
}

function addTestClass(compNum) {
    if (!testClassCounters[compNum]) testClassCounters[compNum] = 0;
    testClassCounters[compNum]++;
    const classNum = testClassCounters[compNum];

    const container = document.getElementById(`testClassesContainer_${compNum}`);
    if (!container) return;

    // Insert new test class before the add button
    const addBtn = container.querySelector('.tc-class-add-btn');
    const html = createTestClassHTML(compNum, classNum);
    addBtn.insertAdjacentHTML('beforebegin', html);

    // Create the first sub-section for this test class
    addSubSection(compNum, classNum);
}

function removeTestClass(compNum, classNum, event) {
    if (event) event.stopPropagation();
    // Count remaining test class sections for this component
    const container = document.getElementById(`testClassesContainer_${compNum}`);
    if (!container) return;
    const sections = container.querySelectorAll('.test-class-section');
    if (sections.length <= 1) return; // Don't remove the last one

    const section = document.getElementById(`testClass_${compNum}_${classNum}`);
    if (section) section.remove();

    // Clean up sub-section counters for this test class
    delete subSectionCounters[`${compNum}_${classNum}`];
}

function toggleTestClassBody(id) {
    const body = document.getElementById(`testClassBody_${id}`);
    const section = document.getElementById(`testClass_${id}`);
    if (!body || !section) return;
    section.classList.toggle('collapsed');
}

function setTestClassBodyDisabled(id, disabled) {
    const section = document.getElementById(`testClass_${id}`);
    if (!section) return;

    // Disable/enable all sub-section prompts within this test class
    const prompts = section.querySelectorAll('textarea[id^="generatorQueryInput_"]');
    prompts.forEach(prompt => {
        prompt.disabled = disabled;
        prompt.style.opacity = disabled ? '0.5' : '1';
        prompt.style.cursor = disabled ? 'not-allowed' : 'text';
    });

    // Disable/enable all action buttons within this test class
    const btnSelector = 'button[id^="runGeneratorBtn_"], button[id^="executeTestBtn_"], button[id^="showReportBtn_"]';
    const buttons = section.querySelectorAll(btnSelector);
    buttons.forEach(btn => {
        btn.disabled = disabled;
        btn.style.opacity = disabled ? '0.5' : '1';
        btn.style.cursor = disabled ? 'not-allowed' : 'pointer';
    });
}

function updateTestClassTitle(id) {
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const section = document.getElementById(`testClass_${id}`);
    if (!titleSpan || !section) return;
    const fileName = section.getAttribute('data-file-name') || `TestFile_${String(id.split('_')[1]).padStart(2, '0')}`;
    const className = section.getAttribute('data-class-name') || 'TestGeneratedAPIs';
    titleSpan.textContent = `📘 ${fileName}::${className}`;
}

function showRenameTestClassInput(id, event) {
    if (event) event.stopPropagation();
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const editor = document.getElementById(`testClassRenameEditor_${id}`);
    const input = document.getElementById(`testClassRenameInput_${id}`);
    if (!titleSpan || !editor || !input) return;

    // Strip emoji prefix for the default value
    const section = document.getElementById(`testClass_${id}`);
    if (!section) return;
    const currentName = section.getAttribute('data-file-name') || '';
    input.value = currentName;

    titleSpan.style.display = 'none';
    editor.style.display = 'inline-flex';
    input.focus();
    input.select();

    // Hide class rename editor if open
    const classEditor = document.getElementById(`testClassClassRenameEditor_${id}`);
    if (classEditor) classEditor.style.display = 'none';

    // Disable the body elements during editing
    setTestClassBodyDisabled(id, true);
}

async function saveTestClassName(id, event) {
    if (event) event.stopPropagation();
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const editor = document.getElementById(`testClassRenameEditor_${id}`);
    const input = document.getElementById(`testClassRenameInput_${id}`);
    if (!titleSpan || !editor || !input) return;

    const newName = input.value.trim();
    if (!newName) {
        alert('Test Class name cannot be empty');
        return;
    }

    // Extract component number and class number from id (format: compNum_classNum)
    const [compNum, classNum] = id.split('_').map(Number);

    const testClassSection = document.getElementById(`testClass_${id}`);
    const existingFileName = (testClassSection ? testClassSection.getAttribute('data-file-name') : null) || `TestFile_${String(classNum).padStart(2, '0')}`;

    // Get the folder name from the component's folder input
    const folderNameInput = document.getElementById(`generatorFolderName_${compNum}`);
    if (!folderNameInput) {
        alert('Could not find folder name for this component');
        return;
    }
    const folderName = folderNameInput.value.trim();

    if (!folderName) {
        alert('Folder name is not set. Please generate test code first.');
        return;
    }
    
    // Show loading state
    const originalText = input.value;
    input.disabled = true;
    input.value = 'Renaming...';

    try {
        // First, check if we should call the backend API or just update the UI
        // If folder name is not set, file doesn't exist yet - just update UI
        let shouldCallBackend = folderName && folderName.length > 0;
        
        if (shouldCallBackend) {
            // Call the backend API to rename the physical file
            const response = await fetch('/rename-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    folder_name: folderName,
                    existing_file_name: existingFileName,
                    new_file_name: newName
                })
            });

            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                const text = await response.text();
                console.error('Non-JSON response received:', text);
                throw new Error('Server returned non-JSON response. Check if Flask server is running.');
            }

            const result = await response.json();

            if (result.success) {
                // Physical file renamed successfully
                titleSpan.style.display = '';
                editor.style.display = 'none';

                if (testClassSection) {
                    const newFileNameWithoutExt = result.new_file_name.replace(/\.py$/, '');
                    testClassSection.setAttribute('data-file-name', newFileNameWithoutExt);
                    // Keep the existing class name; only the file name changed on disk
                    console.log(`Updated data-file-name to: ${newFileNameWithoutExt} (file renamed on disk)`);
                }

                updateTestClassTitle(id);

                // Show success notification
                if (typeof notification !== 'undefined') {
                    notification.success(`File renamed successfully: ${result.old_file_name} → ${result.new_file_name}`);
                } else {
                    alert(`File renamed successfully: ${result.old_file_name} → ${result.new_file_name}`);
                }
            } else {
                // Backend rename failed - check if it's because file doesn't exist
                if (result.message && (result.message.includes('not found') || result.message.includes('does not exist'))) {
                    // File doesn't exist yet - just update UI
                    console.log('File not found on disk - updating UI only (file will be created with new name)');
                    titleSpan.style.display = '';
                    editor.style.display = 'none';

                    if (testClassSection) {
                        testClassSection.setAttribute('data-file-name', newName);
                        const newClassName = deriveClassName(folderName, newName);
                        testClassSection.setAttribute('data-class-name', newClassName);
                        console.log(`Updated data-file-name to: ${newName} (UI only - file doesn't exist yet)`);
                    }

                    updateTestClassTitle(id);
                    
                    // Show info notification
                    if (typeof notification !== 'undefined') {
                        notification.info(`File name updated to '${newName}'. File will be created with this name when you generate code.`);
                    } else {
                        alert(`File name updated to '${newName}'. File will be created with this name when you generate code.`);
                    }
                } else {
                    // Other error - show error and revert
                    if (typeof notification !== 'undefined') {
                        notification.error(`Failed to rename file: ${result.message}`);
                    } else {
                        alert(`Failed to rename file: ${result.message}`);
                    }
                    input.value = originalText;
                }
            }
        } else {
            // Folder name not set - file doesn't exist yet, just update UI
            console.log('Folder name not set - updating UI only (file will be created with new name)');
            titleSpan.style.display = '';
            editor.style.display = 'none';

            if (testClassSection) {
                testClassSection.setAttribute('data-file-name', newName);
                const folderForClass = folderName || `TestComponent_${String(compNum).padStart(2, '0')}`;
                const newClassName = deriveClassName(folderForClass, newName);
                testClassSection.setAttribute('data-class-name', newClassName);
                console.log(`Updated data-file-name to: ${newName} (UI only - no folder set yet)`);
            }

            updateTestClassTitle(id);
            
            // Show info notification
            if (typeof notification !== 'undefined') {
                notification.info(`File name set to '${newName}'. File will be created with this name when you generate code.`);
            } else {
                alert(`File name set to '${newName}'. File will be created with this name when you generate code.`);
            }
        }
    } catch (error) {
        console.error('Error renaming file:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Error renaming file: ${error.message}`);
        } else {
            alert(`Error renaming file: ${error.message}`);
        }
        input.value = originalText;
    } finally {
        // Re-enable input
        input.disabled = false;
        
        // Re-enable the body elements
        setTestClassBodyDisabled(id, false);
    }
}

function cancelRenameTestClass(id, event) {
    if (event) event.stopPropagation();
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const editor = document.getElementById(`testClassRenameEditor_${id}`);
    if (!titleSpan || !editor) return;
    titleSpan.style.display = '';
    editor.style.display = 'none';

    // Re-enable the body elements
    setTestClassBodyDisabled(id, false);
}

function showRenameTestClassNameInput(id, event) {
    if (event) event.stopPropagation();
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const editor = document.getElementById(`testClassClassRenameEditor_${id}`);
    const input = document.getElementById(`testClassClassRenameInput_${id}`);
    const section = document.getElementById(`testClass_${id}`);
    if (!titleSpan || !editor || !input || !section) return;

    const currentClassName = section.getAttribute('data-class-name') || 'TestGeneratedAPIs';
    input.value = currentClassName;

    titleSpan.style.display = 'none';
    editor.style.display = 'inline-flex';
    input.focus();
    input.select();

    // Hide file rename editor if open
    const fileEditor = document.getElementById(`testClassRenameEditor_${id}`);
    if (fileEditor) fileEditor.style.display = 'none';

    // Disable the body elements during editing
    setTestClassBodyDisabled(id, true);
}

async function saveTestClassClassName(id, event) {
    if (event) event.stopPropagation();
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const editor = document.getElementById(`testClassClassRenameEditor_${id}`);
    const input = document.getElementById(`testClassClassRenameInput_${id}`);
    const section = document.getElementById(`testClass_${id}`);
    if (!titleSpan || !editor || !input || !section) return;

    const newClassName = input.value.trim();
    if (!newClassName) {
        alert('Class name cannot be empty');
        return;
    }
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(newClassName)) {
        alert('Class name must be a valid Python identifier');
        return;
    }

    const [compNum, classNum] = id.split('_').map(Number);
    const folderNameInput = document.getElementById(`generatorFolderName_${compNum}`);
    if (!folderNameInput) {
        alert('Could not find folder name for this component');
        return;
    }
    const folderName = folderNameInput.value.trim();
    const fileName = section.getAttribute('data-file-name') || `TestFile_${String(classNum).padStart(2, '0')}`;
    const oldClassName = section.getAttribute('data-class-name') || 'TestGeneratedAPIs';

    const originalText = input.value;
    input.disabled = true;
    input.value = 'Renaming...';

    try {
        const response = await fetch('/rename-class', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                folder_name: folderName,
                file_name: fileName,
                old_class_name: oldClassName,
                new_class_name: newClassName
            })
        });

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            console.error('Non-JSON response received:', text);
            throw new Error('Server returned non-JSON response. Check if Flask server is running.');
        }

        const result = await response.json();

        if (result.success) {
            section.setAttribute('data-class-name', newClassName);
            updateTestClassTitle(id);
            titleSpan.style.display = '';
            editor.style.display = 'none';
            if (typeof notification !== 'undefined') {
                notification.success(`Class renamed successfully: ${oldClassName} → ${newClassName}`);
            } else {
                alert(`Class renamed successfully: ${oldClassName} → ${newClassName}`);
            }
        } else {
            if (result.message && (result.message.includes('not found') || result.message.includes('does not exist'))) {
                console.log('File not found on disk - updating UI only (class will be created with new name)');
                section.setAttribute('data-class-name', newClassName);
                updateTestClassTitle(id);
                titleSpan.style.display = '';
                editor.style.display = 'none';
                if (typeof notification !== 'undefined') {
                    notification.info(`Class name updated to '${newClassName}'. File doesn't exist yet.`);
                } else {
                    alert(`Class name updated to '${newClassName}'. File doesn't exist yet.`);
                }
            } else {
                if (typeof notification !== 'undefined') {
                    notification.error(`Failed to rename class: ${result.message}`);
                } else {
                    alert(`Failed to rename class: ${result.message}`);
                }
                input.value = originalText;
            }
        }
    } catch (error) {
        console.error('Error renaming class:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Error renaming class: ${error.message}`);
        } else {
            alert(`Error renaming class: ${error.message}`);
        }
        input.value = originalText;
    } finally {
        input.disabled = false;
        setTestClassBodyDisabled(id, false);
    }
}

function cancelRenameTestClassName(id, event) {
    if (event) event.stopPropagation();
    const titleSpan = document.getElementById(`testClassTitle_${id}`);
    const editor = document.getElementById(`testClassClassRenameEditor_${id}`);
    if (!titleSpan || !editor) return;
    titleSpan.style.display = '';
    editor.style.display = 'none';

    // Re-enable the body elements
    setTestClassBodyDisabled(id, false);
}

function deleteTestFile(id, event) {
    if (event) event.stopPropagation();

    const [compNum, classNum] = id.split('_').map(Number);

    // Get the folder name from the component's folder input
    const folderNameInput = document.getElementById(`generatorFolderName_${compNum}`);
    if (!folderNameInput) {
        alert('Could not find folder name for this component');
        return;
    }
    const folderName = folderNameInput.value.trim();
    if (!folderName) {
        alert('Folder name is not set. No file to delete.');
        return;
    }

    // Get the test class section and file name
    const testClassSection = document.getElementById(`testClass_${id}`);
    if (!testClassSection) {
        alert('Could not find test class section');
        return;
    }

    const fileName = testClassSection.getAttribute('data-file-name');
    if (!fileName) {
        alert('No file name found for this test class');
        return;
    }

    if (!confirm(`Are you sure you want to delete file "${fileName}.py"?`)) {
        return;
    }

    // Send request to backend to delete the file
    fetch('/delete-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder_name: folderName,
            file_name: fileName
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Remove the test class section from the UI
            testClassSection.remove();
            if (typeof notification !== 'undefined') {
                notification.success(`File deleted successfully: ${fileName}.py`);
            } else {
                alert(`File deleted successfully: ${fileName}.py`);
            }
        } else {
            if (typeof notification !== 'undefined') {
                notification.error(`Failed to delete file: ${result.message}`);
            } else {
                alert(`Failed to delete file: ${result.message}`);
            }
        }
    })
    .catch(error => {
        console.error('Error deleting file:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Error deleting file: ${error.message}`);
        } else {
            alert(`Error deleting file: ${error.message || 'Please try again.'}`);
        }
    });
}

// ===== Sub Section rename helpers =====

function setSubSectionBodyDisabled(id, subNum, disabled) {
    const subId = `${id}_${subNum}`;
    const prompt = document.getElementById(`generatorQueryInput_${subId}`);
    const runBtn = document.getElementById(`runGeneratorBtn_${subId}`);
    const execBtn = document.getElementById(`executeTestBtn_${subId}`);
    const reportBtn = document.getElementById(`showReportBtn_${subId}`);

    if (prompt) {
        prompt.disabled = disabled;
        prompt.style.opacity = disabled ? '0.5' : '1';
        prompt.style.cursor = disabled ? 'not-allowed' : 'text';
    }
    [runBtn, execBtn, reportBtn].forEach(btn => {
        if (btn) {
            btn.disabled = disabled;
            btn.style.opacity = disabled ? '0.5' : '1';
            btn.style.cursor = disabled ? 'not-allowed' : 'pointer';
        }
    });
}

function showRenameSubSectionInput(id, subNum, event) {
    if (event) event.stopPropagation();
    const subId = `${id}_${subNum}`;
    const renameLink = document.getElementById(`subSectionRenameLink_${subId}`);
    if (renameLink && renameLink.classList.contains('sub-section-rename-disabled')) return;
    const titleSpan = document.getElementById(`subSectionTitle_${subId}`);
    const editor = document.getElementById(`subSectionRenameEditor_${subId}`);
    const input = document.getElementById(`subSectionRenameInput_${subId}`);
    if (!titleSpan || !editor || !input) return;

    // Extract the current method name to show in placeholder
    const currentText = titleSpan.textContent;
    const methodNameMatch = currentText.match(/:\s*(.+)$/);
    const currentMethodName = methodNameMatch ? methodNameMatch[1].trim() : '';
    
    // Clear input and set placeholder to show current method name
    input.value = '';
    input.placeholder = `Current: ${currentMethodName}`;

    titleSpan.style.display = 'none';
    editor.style.display = 'inline-flex';
    input.focus();

    // Disable the body elements during editing
    setSubSectionBodyDisabled(id, subNum, true);
}

function saveSubSectionName(id, subNum, event) {
    if (event) event.stopPropagation();
    const subId = `${id}_${subNum}`;
    const titleSpan = document.getElementById(`subSectionTitle_${subId}`);
    const editor = document.getElementById(`subSectionRenameEditor_${subId}`);
    const input = document.getElementById(`subSectionRenameInput_${subId}`);
    if (!titleSpan || !editor || !input) {
        console.error('Missing elements:', { titleSpan, editor, input });
        return;
    }

    const appendText = input.value.trim();
    console.log('Append text:', appendText);
    if (!appendText) {
        alert('Append text cannot be empty');
        return;
    }

    // Extract the current method name from the title (format: "📝 TestMethod_01 : method_name")
    const currentTitle = titleSpan.textContent;
    console.log('Current title:', currentTitle);
    const methodNameMatch = currentTitle.match(/:\s*(.+)$/);
    console.log('Method name match:', methodNameMatch);
    if (!methodNameMatch) {
        alert('No method name found. Please generate test code first.');
        return;
    }

    const oldMethodName = methodNameMatch[1].trim();
    const [compNum, classNum] = id.split('_');
    const folderInput = document.getElementById(`generatorFolderName_${compNum}`);
    const testClassSection = document.getElementById(`testClass_${id}`);
    const folderName = (folderInput ? folderInput.value.trim() : '') || `TestComponent_${String(compNum).padStart(2, '0')}`;
    const fileName = (testClassSection ? testClassSection.getAttribute('data-file-name') : null) || `TestFile_${String(classNum).padStart(2, '0')}`;
    console.log('Extracted data:', { oldMethodName, compNum, classNum, folderName, fileName });

    // Show loading state
    input.disabled = true;
    const saveBtn = event.target;
    const originalText = saveBtn.textContent;
    saveBtn.textContent = '⏳';

    // Send request to backend to rename the method
    console.log('Sending rename request:', { folderName, fileName, oldMethodName, appendText });
    fetch('/rename-method', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder_name: folderName,
            file_name: fileName,
            old_method_name: oldMethodName,
            append_text: appendText
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(result => {
        console.log('Rename result:', result);
        if (result.success) {
            // Update the title with the new method name
            const emojiPrefix = currentTitle.match(/^[^\p{L}\p{N}]+\s*/u)?.[0] || '';
            const labelPart = currentTitle.replace(/^[^\p{L}\p{N}]+\s*/u, '').split(/\s*:\s*/)[0].trim();
            titleSpan.textContent = `${emojiPrefix}${labelPart} : ${result.new_method_name}`;
            titleSpan.style.display = '';
            editor.style.display = 'none';

            // Update the tracked method name
            const subSection = document.getElementById(`subSection_${subId}`);
            if (subSection) {
                subSection.setAttribute('data-method-name', result.new_method_name);
            }

            setSubSectionBodyDisabled(id, subNum, false);
        } else {
            alert(`Failed to rename method: ${result.message}`);
            input.disabled = false;
            saveBtn.textContent = originalText;
        }
    })
    .catch(error => {
        console.error('Error renaming method:', error);
        alert(`Error renaming method: ${error.message || 'Please try again.'}`);
        input.disabled = false;
        saveBtn.textContent = originalText;
    });
}

function cancelRenameSubSection(id, subNum, event) {
    if (event) event.stopPropagation();
    const subId = `${id}_${subNum}`;
    const titleSpan = document.getElementById(`subSectionTitle_${subId}`);
    const editor = document.getElementById(`subSectionRenameEditor_${subId}`);
    if (!titleSpan || !editor) return;
    titleSpan.style.display = '';
    editor.style.display = 'none';

    // Re-enable the body elements
    setSubSectionBodyDisabled(id, subNum, false);
}

function deleteTestMethod(id, subNum, event) {
    if (event) event.stopPropagation();
    const subId = `${id}_${subNum}`;
    const titleSpan = document.getElementById(`subSectionTitle_${subId}`);
    const deleteLink = document.getElementById(`subSectionDeleteLink_${subId}`);
    if (deleteLink && deleteLink.classList.contains('sub-section-delete-disabled')) return;

    if (!titleSpan) return;

    const currentTitle = titleSpan.textContent;
    const methodNameMatch = currentTitle.match(/:\s*(.+)$/);
    if (!methodNameMatch) {
        alert('No method name found. Please generate test code first.');
        return;
    }

    const methodName = methodNameMatch[1].trim();
    const [compNum, classNum] = id.split('_');
    const folderInput = document.getElementById(`generatorFolderName_${compNum}`);
    const testClassSection = document.getElementById(`testClass_${id}`);
    const folderName = (folderInput ? folderInput.value.trim() : '') || `TestComponent_${String(compNum).padStart(2, '0')}`;
    const fileName = (testClassSection ? testClassSection.getAttribute('data-file-name') : null) || `TestFile_${String(classNum).padStart(2, '0')}`;

    if (!confirm(`Are you sure you want to delete method "${methodName}"?`)) {
        return;
    }

    // Send request to backend to delete the method
    fetch('/delete-method', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder_name: folderName,
            file_name: fileName,
            method_name: methodName
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Revert title to the original placeholder (remove the method name)
            titleSpan.textContent = currentTitle.split(' : ')[0];

            // Remove the tracked method name
            const subSection = document.getElementById(`subSection_${subId}`);
            if (subSection) {
                subSection.removeAttribute('data-method-name');
            }

            // Disable the delete and rename links since no method exists anymore
            if (deleteLink) {
                deleteLink.classList.add('sub-section-delete-disabled');
                deleteLink.title = 'Generate test code first to enable';
            }

            const renameLink = document.getElementById(`subSectionRenameLink_${subId}`);
            if (renameLink) {
                renameLink.classList.add('sub-section-rename-disabled');
                renameLink.title = 'Generate test code first to enable';
            }

            alert(`Method "${methodName}" deleted successfully`);
        } else {
            alert(`Failed to delete method: ${result.message}`);
        }
    })
    .catch(error => {
        console.error('Error deleting method:', error);
        alert(`Error deleting method: ${error.message || 'Please try again.'}`);
    });
}

function createTestComponentHTML(num) {
    return `
        <div class="input-section">
            <input type="hidden" id="generatorFolderName_${num}" value="">
            <input type="checkbox" id="useComponentAsFolder_${num}" checked style="display: none;">

            <div style="margin: 10px 0;">
                <a href="javascript:void(0)" class="component-delete-link" onclick="deleteTestComponent(${num}, event)" title="Delete this component folder and all its files">Delete Component/Folder</a>
                <a href="javascript:void(0)" class="component-clear-link" onclick="clearExecutionResults(${num}, event)" title="Clear allure-results and allure-report folders" style="margin-left: 12px;">Clear Execution Results</a>
                <a href="javascript:void(0)" class="component-report-link" onclick="generateAllureReport(${num}, event)" title="Generate Allure report from existing results" style="margin-left: 12px;">Generate Reports</a>
            </div>

            <div class="test-classes-container" id="testClassesContainer_${num}">
                <button class="tc-class-add-btn" onclick="addTestClass(${num})" title="Add new Test Class">+ Add Test Class</button>
            </div>
        </div>
    `;
}

function createTestComponentTabHTML(num) {
    const closeBtn = `<button class="tc-tab-close" onclick="removeTestComponent(${num}, event)" title="Remove">&times;</button>`;
    return `
        <div class="tc-tab active" id="tcTab_${num}" onclick="switchTestComponent(${num})" ondblclick="renameTestComponent(${num})" title="Double-click to rename">
            <span id="tcTabLabel_${num}">🛠️ TestComponent_${String(num).padStart(2, '0')}</span>
            ${closeBtn}
        </div>
    `;
}

function createIconsGroupHTML() {
    return `
        <span class="tc-icons-group" onclick="event.stopPropagation()" ondblclick="event.stopPropagation()">
            <span class="tc-help-icon" title="Double-click a tab to rename it. Click + to add a new TestComponent. Click × to remove a tab.">?</span>
            <button class="tc-add-btn" onclick="event.stopPropagation(); addTestComponent()" title="Add new TestComponent">+</button>
        </span>
    `;
}

function moveIconsGroupToLastTab() {
    const iconsGroup = document.querySelector('.tc-icons-group');
    if (!iconsGroup) return;
    const allTabs = document.querySelectorAll('.tc-tab');
    if (allTabs.length === 0) return;
    const lastTab = allTabs[allTabs.length - 1];
    lastTab.appendChild(iconsGroup);
}

async function renameTestComponent(num) {
    const labelSpan = document.getElementById(`tcTabLabel_${num}`);
    const folderInput = document.getElementById(`generatorFolderName_${num}`);
    const checkbox = document.getElementById(`useComponentAsFolder_${num}`);
    if (!labelSpan || !folderInput) return;

    const currentText = labelSpan.textContent;
    // Strip leading emoji/icon for the prompt default
    const currentName = currentText.replace(/^[^\p{L}\p{N}]+\s*/u, '');
    const oldFolderName = folderInput.value.trim() || currentName;

    const newName = prompt('Enter new name for this tab:', currentName);
    if (newName === null) return; // User cancelled
    const trimmed = newName.trim();
    if (!trimmed) {
        alert('Tab name cannot be empty');
        return;
    }

    // If "Use Component as folder" is checked and the folder name would change,
    // call the backend to rename the physical rest_test folder (if it exists)
    if (checkbox && checkbox.checked && oldFolderName !== trimmed) {
        try {
            const response = await fetch('/rename-component', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    old_folder_name: oldFolderName,
                    new_folder_name: trimmed
                })
            });
            const result = await response.json();

            if (!result.success) {
                if (typeof notification !== 'undefined') {
                    notification.error(`Failed to rename folder: ${result.message}`);
                } else {
                    alert(`Failed to rename folder: ${result.message}`);
                }
                return;
            }

            console.log(`Component folder renamed: ${oldFolderName} -> ${trimmed}`);
        } catch (error) {
            console.error('Error renaming component folder:', error);
            if (typeof notification !== 'undefined') {
                notification.error(`Error renaming component folder: ${error.message || 'Please try again.'}`);
            } else {
                alert(`Error renaming component folder: ${error.message || 'Please try again.'}`);
            }
            return;
        }
    }

    // Update tab label
    labelSpan.textContent = `🛠️ ${trimmed}`;

    // If "Use Component as folder" is checked, sync the folder name with the new tab name
    if (checkbox && checkbox.checked) {
        onUseComponentAsFolderChange(num);
    }
}

function onUseComponentAsFolderChange(num) {
    const checkbox = document.getElementById(`useComponentAsFolder_${num}`);
    const folderInput = document.getElementById(`generatorFolderName_${num}`);
    if (!checkbox || !folderInput) return;

    if (checkbox.checked) {
        // Use the tab name as the folder name
        const labelSpan = document.getElementById(`tcTabLabel_${num}`);
        if (labelSpan) {
            const tabName = labelSpan.textContent.replace(/^[^\p{L}\p{N}]+\s*/u, '');
            folderInput.value = tabName;
        }
        folderInput.readOnly = true;
        folderInput.style.opacity = '0.6';
        folderInput.style.cursor = 'not-allowed';
    } else {
        // Allow manual entry
        folderInput.readOnly = false;
        folderInput.style.opacity = '1';
        folderInput.style.cursor = 'text';
    }

    updateComponentClassNames(num);
}

function addTestComponent() {
    testComponentCounter++;
    const num = testComponentCounter;

    // Deactivate all existing tabs and panels
    document.querySelectorAll('.tc-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.test-component-panel').forEach(p => p.classList.remove('active'));

    // Add new tab to the container
    const tabsContainer = document.getElementById('testComponentTabs');
    const tabHTML = createTestComponentTabHTML(num);
    tabsContainer.insertAdjacentHTML('beforeend', tabHTML);

    // Create icons group if it doesn't exist yet, then move it into the new last tab
    if (!document.querySelector('.tc-icons-group')) {
        tabsContainer.insertAdjacentHTML('beforeend', createIconsGroupHTML());
    }
    moveIconsGroupToLastTab();

    // Add new panel
    const contentArea = document.getElementById('testComponentContentArea');
    const panel = document.createElement('div');
    panel.className = 'test-component-panel active';
    panel.id = `tcPanel_${num}`;
    panel.innerHTML = createTestComponentHTML(num);
    contentArea.appendChild(panel);

    // Create the first test class for this component
    testClassCounters[num] = 0;
    addTestClass(num);

    // Sync folder name with tab name (checkbox is checked by default)
    onUseComponentAsFolderChange(num);

    activeTestComponent = num;
}

function switchTestComponent(num) {
    // Deactivate all tabs and panels
    document.querySelectorAll('.tc-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.test-component-panel').forEach(p => p.classList.remove('active'));

    // Activate selected
    const tab = document.getElementById(`tcTab_${num}`);
    const panel = document.getElementById(`tcPanel_${num}`);
    if (tab) tab.classList.add('active');
    if (panel) panel.classList.add('active');

    activeTestComponent = num;
}

function removeTestComponent(num, event) {
    if (event) event.stopPropagation();
    // Count actual tabs in DOM
    const allTabs = document.querySelectorAll('.tc-tab');
    if (allTabs.length <= 1) return; // Don't remove the last one

    // Detach the icons group BEFORE removing the tab (so it doesn't get deleted)
    const iconsGroup = document.querySelector('.tc-icons-group');
    if (iconsGroup) {
        iconsGroup.remove(); // Detach from DOM but keep the element reference
    }

    // Remove tab and panel
    const tab = document.getElementById(`tcTab_${num}`);
    const panel = document.getElementById(`tcPanel_${num}`);
    if (tab) tab.remove();
    if (panel) panel.remove();

    // Re-insert the icons group into the tabs container, then move to last tab
    const tabsContainer = document.getElementById('testComponentTabs');
    if (iconsGroup && tabsContainer) {
        tabsContainer.appendChild(iconsGroup);
    }
    moveIconsGroupToLastTab();

    // If we removed the active one, switch to the first available
    if (activeTestComponent === num) {
        const firstTab = document.querySelector('.tc-tab');
        if (firstTab) {
            const firstNum = parseInt(firstTab.id.replace('tcTab_', ''));
            switchTestComponent(firstNum);
        }
    }

    // Clean up test class counter for this component
    delete testClassCounters[num];

    // Clean up sub-section counters for all test classes in this component
    Object.keys(subSectionCounters).forEach(key => {
        if (key.startsWith(`${num}_`)) {
            delete subSectionCounters[key];
        }
    });
}

function deleteTestComponent(num, event) {
    if (event) event.stopPropagation();

    const folderNameInput = document.getElementById(`generatorFolderName_${num}`);
    if (!folderNameInput) {
        alert('Could not find folder name for this component');
        return;
    }
    const folderName = folderNameInput.value.trim();
    if (!folderName) {
        alert('Folder name is not set. No component to delete.');
        return;
    }

    if (!confirm(`Are you sure you want to delete component folder "${folderName}" and all its files?`)) {
        return;
    }

    // Send request to backend to delete the component folder
    fetch('/delete-component', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder_name: folderName
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Remove the component tab and panel from the UI
            removeTestComponent(num, null);
            if (typeof notification !== 'undefined') {
                notification.success(`Component folder deleted successfully: ${folderName}`);
            } else {
                alert(`Component folder deleted successfully: ${folderName}`);
            }
        } else {
            if (typeof notification !== 'undefined') {
                notification.error(`Failed to delete component: ${result.message}`);
            } else {
                alert(`Failed to delete component: ${result.message}`);
            }
        }
    })
    .catch(error => {
        console.error('Error deleting component:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Error deleting component: ${error.message}`);
        } else {
            alert(`Error deleting component: ${error.message || 'Please try again.'}`);
        }
    });
}

async function clearExecutionResults(num, event) {
    if (event) event.stopPropagation();

    if (!confirm('Are you sure you want to clear allure results and reports?')) {
        return;
    }

    try {
        const response = await fetch('/clear-execution-results', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const result = await response.json();

        if (result.success) {
            if (typeof notification !== 'undefined') {
                notification.success(result.message);
            } else {
                alert(result.message);
            }
        } else {
            if (typeof notification !== 'undefined') {
                notification.error(`Failed to clear results: ${result.message}`);
            } else {
                alert(`Failed to clear results: ${result.message}`);
            }
        }
    } catch (error) {
        console.error('Error clearing execution results:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Error clearing results: ${error.message}`);
        } else {
            alert(`Error clearing results: ${error.message || 'Please try again.'}`);
        }
    }
}

async function generateAllureReport(num, event) {
    if (event) event.stopPropagation();

    try {
        const response = await fetch('/show-allure-report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const result = await response.json();

        if (result.success) {
            if (typeof notification !== 'undefined') {
                notification.success(result.message);
            }

            if (result.url) {
                const newWindow = window.open(result.url, '_blank');
                if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {
                    console.warn('Popup blocked!');
                    if (typeof notification !== 'undefined') {
                        notification.info(`Report generated: <a href="${result.url}" target="_blank">Open Report</a>`);
                    } else {
                        alert(`Report generated. Click to open: ${result.url}`);
                    }
                }
            }
        } else {
            if (typeof notification !== 'undefined') {
                notification.error(`Report generation failed: ${result.message}`);
            } else {
                alert(`Report generation failed: ${result.message}`);
            }
        }
    } catch (error) {
        console.error('Error generating Allure report:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Error generating report: ${error.message}`);
        } else {
            alert(`Error generating report: ${error.message || 'Please try again.'}`);
        }
    }
}

function initTestComponents() {
    // Clear the tabs container
    const tabsContainer = document.getElementById('testComponentTabs');
    tabsContainer.innerHTML = '';
    // Create the first component (icons group will be moved inside it)
    addTestComponent();
}

async function loadExistingTests() {
    const btn = document.getElementById('loadExistingTestsBtn');
    if (btn) {
        btn.disabled = true;
        btn.textContent = '⏳ Loading...';
    }

    try {
        const response = await fetch('/load-existing-tests');
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            throw new Error('Server returned non-JSON response. Check if Flask server is running.');
        }

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.message || 'Failed to load existing tests');
        }

        // Reset the UI state
        testComponentCounter = 0;
        activeTestComponent = 1;
        testClassCounters = {};
        subSectionCounters = {};

        const tabsContainer = document.getElementById('testComponentTabs');
        const contentArea = document.getElementById('testComponentContentArea');
        tabsContainer.innerHTML = '';
        contentArea.innerHTML = '';

        // Build each component
        (result.components || []).forEach((component) => {
            // Add a new component using the existing builder
            addTestComponent();
            const compNum = testComponentCounter;

            // Set the tab label and sync folder name
            const tabLabel = document.getElementById(`tcTabLabel_${compNum}`);
            if (tabLabel) tabLabel.textContent = `🛠️ ${component.name}`;
            onUseComponentAsFolderChange(compNum);

            const files = component.files || [];
            files.forEach((file, fIdx) => {
                // The first file reuses the default class created by addTestComponent
                if (fIdx > 0) {
                    addTestClass(compNum);
                }

                const classNum = testClassCounters[compNum];
                const id = `${compNum}_${classNum}`;
                const section = document.getElementById(`testClass_${id}`);
                if (section) {
                    section.setAttribute('data-file-name', file.file_name);
                    const className = file.class_name || deriveClassName(component.name, file.file_name);
                    section.setAttribute('data-class-name', className);
                    updateTestClassTitle(id);
                }

                const methods = file.methods || [];
                const subContainer = document.getElementById(`subSectionsContainer_${id}`);
                if (subContainer) {
                    const existingSubSections = subContainer.querySelectorAll('.sub-section');
                    for (let mIdx = existingSubSections.length; mIdx < methods.length; mIdx++) {
                        addSubSection(compNum, classNum);
                    }

                    const subSections = subContainer.querySelectorAll('.sub-section');
                    subSections.forEach((sub, mIdx) => {
                        const subNum = mIdx + 1;
                        const subId = `${id}_${subNum}`;
                        const methodData = methods[mIdx];
                        const titleSpan = document.getElementById(`subSectionTitle_${subId}`);
                        const deleteLink = document.getElementById(`subSectionDeleteLink_${subId}`);
                        const renameLink = document.getElementById(`subSectionRenameLink_${subId}`);
                        const queryInput = document.getElementById(`generatorQueryInput_${subId}`);

                        if (methodData && titleSpan) {
                            const methodName = methodData.name || `TestMethod_${String(subNum).padStart(2, '0')}`;
                            titleSpan.textContent = `📝 TestMethod_${String(subNum).padStart(2, '0')} : ${methodName}`;
                            sub.setAttribute('data-method-name', methodName);

                            if (queryInput && methodData.prompt) {
                                queryInput.value = methodData.prompt;
                            }
                        }

                        // Loaded methods are real, so enable delete/rename links
                        if (deleteLink) {
                            deleteLink.classList.remove('sub-section-delete-disabled');
                            deleteLink.title = 'Delete Method';
                        }
                        if (renameLink) {
                            renameLink.classList.remove('sub-section-rename-disabled');
                            renameLink.title = 'Append Method Name';
                        }
                    });
                }
            });
        });

        // Ensure the icons group is on the last tab
        moveIconsGroupToLastTab();

        // Activate the first loaded component
        if (testComponentCounter > 0) {
            switchTestComponent(1);
        }
    } catch (error) {
        console.error('Error loading existing tests:', error);
        if (typeof notification !== 'undefined') {
            notification.error(`Failed to load existing tests: ${error.message}`);
        } else {
            alert(`Failed to load existing tests: ${error.message}`);
        }
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.textContent = '📂 Load Existing Tests';
        }
    }
}

function updatePromptSidecar(compNum, classNum, subNum) {
    const id = `${compNum}_${classNum}`;
    const subId = `${id}_${subNum}`;
    const subSection = document.getElementById(`subSection_${subId}`);
    const testClassSection = document.getElementById(`testClass_${id}`);
    const folderInput = document.getElementById(`generatorFolderName_${compNum}`);
    const queryInput = document.getElementById(`generatorQueryInput_${subId}`);
    if (!subSection || !testClassSection || !folderInput || !queryInput) return;

    const methodName = subSection.getAttribute('data-method-name');
    if (!methodName) return; // not a real generated method yet

    const folderName = folderInput.value.trim();
    const fileName = testClassSection.getAttribute('data-file-name');
    const className = testClassSection.getAttribute('data-class-name');
    const prompt = queryInput.value;

    fetch('/update-prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder_name: folderName,
            file_name: fileName,
            class_name: className,
            method_name: methodName,
            prompt: prompt
        })
    })
    .then(response => response.json())
    .then(result => {
        if (!result.success) {
            console.warn('Failed to update prompt sidecar:', result.message);
        }
    })
    .catch(error => {
        console.error('Error updating prompt sidecar:', error);
    });
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

    // Get filename prefix from checkbox or input field
    const checkboxChecked = document.getElementById('swaggerDefaultFileNameCheckbox')?.checked;
    const inputValue = document.getElementById('swaggerFilePrefixInput')?.value.trim();
    const filenamePrefix = checkboxChecked ? 'Swagger_Data' : (inputValue || 'Swagger_Data');
    
    console.log('🔍 DEBUG (script.js): Checkbox checked:', checkboxChecked);
    console.log('🔍 DEBUG (script.js): Input value:', inputValue);
    console.log('🔍 DEBUG (script.js): Final filename prefix:', filenamePrefix);

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
            body: JSON.stringify({ url: url, filename_prefix: filenamePrefix })
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
    const fileInput = document.getElementById('jsonFileInput');
    const runBtn = document.getElementById('runJsonParserBtn');
    const statusSection = document.getElementById('statusSection');
    const resultsSection = document.getElementById('resultsSection');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');

    const url = urlInput ? urlInput.value.trim() : '';
    const file = fileInput && fileInput.files ? fileInput.files[0] : null;

    if (!url && !file) {
        alert('Please enter an OpenAPI spec URL or upload a JSON file');
        return;
    }

    // Get filename prefix from checkbox or input field
    const checkboxChecked = document.getElementById('jsonDefaultFileNameCheckbox')?.checked;
    const inputValue = document.getElementById('jsonFilePrefixInput')?.value.trim();
    const filenamePrefix = checkboxChecked ? 'OpenAPI_Data' : (inputValue || 'OpenAPI_Data');
    
    console.log('🔍 DEBUG (script.js): Checkbox checked:', checkboxChecked);
    console.log('🔍 DEBUG (script.js): Input value:', inputValue);
    console.log('🔍 DEBUG (script.js): Final filename prefix:', filenamePrefix);

    let bodyData = {};
    let requestType = 'url';

    if (file) {
        // Read the uploaded JSON file
        const fileContent = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });

        bodyData = {
            type: 'file',
            filename: file.name,
            content: fileContent,
            filename_prefix: filenamePrefix
        };
        requestType = 'file';
    } else {
        bodyData = {
            type: 'url',
            url: url,
            filename_prefix: filenamePrefix
        };
    }

    // Show loading state
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Running...';
    statusSection.style.display = 'block';
    statusSection.className = 'status-section';
    statusIcon.textContent = '⏳';
    statusIcon.className = 'spinning';
    statusText.textContent = requestType === 'file' ? 'Parsing uploaded OpenAPI JSON...' : 'Parsing OpenAPI JSON... This should take ~1 second';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/run-json-parser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
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

async function runGenerator(compNum, classNum, subNum) {
    const num = compNum || activeTestComponent || 1;
    const cls = classNum || (testClassCounters[num] ? testClassCounters[num] : 1);
    const sub = subNum || (subSectionCounters[`${num}_${cls}`] ? subSectionCounters[`${num}_${cls}`] : 1);
    const id = `${num}_${cls}`;
    const subId = `${id}_${sub}`;
    const excelFileSelect = document.getElementById('generatorExcelFileSelect');
    const baseUrlSelect = document.getElementById('generatorBaseUrlSelect');
    const customBaseUrlInput = document.getElementById('generatorCustomBaseUrl');
    const folderNameInput = document.getElementById(`generatorFolderName_${num}`);
    const queryInput = document.getElementById(`generatorQueryInput_${subId}`);
    const runBtn = document.getElementById(`runGeneratorBtn_${subId}`);
    const statusSection = document.getElementById(`generatorStatus_${subId}`);
    const statusIcon = document.getElementById(`generatorStatusIcon_${subId}`);
    const statusText = document.getElementById(`generatorStatusText_${subId}`);

    // Get the actual file name from the test class section's data attribute
    const testClassSection = document.getElementById(`testClass_${id}`);
    const fileName = testClassSection ? testClassSection.getAttribute('data-file-name') : `TestFile_${String(cls).padStart(2, '0')}`;
    console.log(`Generate Test - Using file name: ${fileName}`);

    const excelPath = excelFileSelect.value;
    let baseUrl = baseUrlSelect.value;
    const folderName = folderNameInput.value.trim();
    const query = queryInput.value.trim();
    const aiModel = getSelectedAiModel();

    // Check if the method already exists and confirm replacement
    const subSection = document.getElementById(`subSection_${subId}`);
    const existingMethodName = subSection ? subSection.getAttribute('data-method-name') : null;
    let replaceMethod = false;
    if (existingMethodName) {
        const confirmed = confirm(`Method code for "${existingMethodName}" already exists. Do you want to replace it?`);
        if (!confirmed) {
            return;
        }
        replaceMethod = true;
    }

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
                ai_model: aiModel,
                replace_method: replaceMethod,
                method_name: existingMethodName || null
            })
        });

        const result = await response.json();

        // Update status
        statusIcon.className = '';
        if (result.success) {
            statusSection.className = 'status-section success';
            statusIcon.textContent = '✅';
            statusText.textContent = 'Test code generated successfully!';

            // Update sub-section title to show the generated method name
            const subTitleSpan = document.getElementById(`subSectionTitle_${subId}`);
            if (subTitleSpan) {
                // Determine the final method name (prefer AI-modified version if present)
                let generatedMethodName = '';
                if (result.generated_code && result.generated_code.length > 0) {
                    // Find AI-modified method, otherwise use the last method
                    const aiMethod = result.generated_code.find(m => m.ai_modified);
                    generatedMethodName = aiMethod ? aiMethod.method_name : result.generated_code[result.generated_code.length - 1].method_name;
                } else if (result.generated_method_names && result.generated_method_names.length > 0) {
                    generatedMethodName = result.generated_method_names[result.generated_method_names.length - 1];
                }

                if (generatedMethodName) {
                    // Preserve the emoji prefix and original label, append the method name
                    const currentText = subTitleSpan.textContent;
                    const emojiPrefix = currentText.match(/^[^\p{L}\p{N}]+\s*/u)?.[0] || '';
                    const labelPart = currentText.replace(/^[^\p{L}\p{N}]+\s*/u, '').split(/\s*:\s*/)[0].trim();
                    subTitleSpan.textContent = `${emojiPrefix}${labelPart} : ${generatedMethodName}`;

                    // Track the method name for prompt sidecar updates
                    const subSection = document.getElementById(`subSection_${subId}`);
                    if (subSection) {
                        subSection.setAttribute('data-method-name', generatedMethodName);
                    }

                    // Enable the "Append Text" and "Delete Method" links now that a method name exists
                    const renameLink = document.getElementById(`subSectionRenameLink_${subId}`);
                    if (renameLink) {
                        renameLink.classList.remove('sub-section-rename-disabled');
                        renameLink.title = 'Append Method Name';
                    }

                    const deleteLink = document.getElementById(`subSectionDeleteLink_${subId}`);
                    if (deleteLink) {
                        deleteLink.classList.remove('sub-section-delete-disabled');
                        deleteLink.title = 'Delete Method';
                    }
                }
            }

            // Update test class title with generated class name
            const testClassSection = document.getElementById(`testClass_${id}`);
            if (testClassSection && result.class_name) {
                testClassSection.setAttribute('data-class-name', result.class_name);
                console.log(`Updated data-class-name to: ${result.class_name}`);
                updateTestClassTitle(id);
            }

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
        const outputTabsContainer = document.getElementById(`outputTabsContainer_${subId}`);
        console.log('Output tabs container:', outputTabsContainer);
        outputTabsContainer.style.display = 'block';

        // Switch to generation results tab
        switchOutputTab(`generation-results_${subId}`, num, cls, sub);

        const generationResultsContent = document.getElementById(`generationResultsContent_${subId}`);
        console.log('Generation results content element:', generationResultsContent);

        let resultsHTML = '';

        if (result.success && result.file_path) {
            resultsHTML += `<div class="result-item"><strong>📄 Generated File:</strong> ${result.file_path}</div>`;
            resultsHTML += `<div class="result-item"><strong>📁 Folder:</strong> ${result.folder_path}</div>`;
            resultsHTML += `<div class="result-item"><strong>🧪 Tests Generated:</strong> ${result.tests_generated}</div>`;

            if (result.class_name) {
                resultsHTML += `<div class="result-item"><strong>🏷️ Class Name:</strong> ${result.class_name}</div>`;
            }

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
        const executionLogsContent = document.getElementById(`executionLogsContent_${subId}`);
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

    // Initialize TestComponent sub-tabs
    initTestComponents();

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

async function executeGeneratedTest(compNum, classNum, subNum) {
    const num = compNum || activeTestComponent || 1;
    const cls = classNum || (testClassCounters[num] ? testClassCounters[num] : 1);
    const sub = subNum || (subSectionCounters[`${num}_${cls}`] ? subSectionCounters[`${num}_${cls}`] : 1);
    const id = `${num}_${cls}`;
    const subId = `${id}_${sub}`;
    const executeBtn = document.getElementById(`executeTestBtn_${subId}`);
    const statusSection = document.getElementById(`generatorStatus_${subId}`);
    const statusIcon = document.getElementById(`generatorStatusIcon_${subId}`);
    const statusText = document.getElementById(`generatorStatusText_${subId}`);

    // Get folder name from UI; get actual file name from data attribute
    const folderNameInput = document.getElementById(`generatorFolderName_${num}`);
    const folderName = folderNameInput.value.trim();

    // Get the actual file name from the test class section's data attribute
    const testClassSection = document.getElementById(`testClass_${id}`);
    const fileName = testClassSection ? testClassSection.getAttribute('data-file-name') : `TestFile_${String(cls).padStart(2, '0')}`;
    console.log(`Execute Test - Using file name: ${fileName}`);

    // Extract the generated method name from the sub-section title
    // Format after generation: "📝 TestMethod_01 : test_01_..._ai"
    const subTitleSpan = document.getElementById(`subSectionTitle_${subId}`);
    let methodName = null;
    if (subTitleSpan) {
        const titleText = subTitleSpan.textContent;
        console.log(`Execute Test - sub-section title text: "${titleText}"`);
        const colonIndex = titleText.indexOf(':');
        if (colonIndex !== -1) {
            methodName = titleText.substring(colonIndex + 1).trim();
        }
    }
    console.log(`Execute Test - extracted method_name: "${methodName}"`);

    // Validation
    if (!folderName) {
        alert('Please enter a folder name');
        return;
    }

    if (!methodName) {
        alert('Please generate test code first to create a test method');
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
                file_name: fileName,
                method_name: methodName
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
            const outputTabsContainer = document.getElementById(`outputTabsContainer_${subId}`);
            outputTabsContainer.style.display = 'block';

            // Switch to execution logs tab
            switchOutputTab(`execution-logs_${subId}`, num, cls, sub);

            // Show test output in execution logs
            const executionLogsContent = document.getElementById(`executionLogsContent_${subId}`);
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
            const outputTabsContainer = document.getElementById(`outputTabsContainer_${subId}`);
            outputTabsContainer.style.display = 'block';

            // Switch to execution logs tab
            switchOutputTab(`execution-logs_${subId}`, num, cls, sub);

            // Show error in execution logs
            const executionLogsContent = document.getElementById(`executionLogsContent_${subId}`);
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

async function executeClassTests(compNum, classNum, event) {
    if (event) event.stopPropagation();

    const num = compNum || activeTestComponent || 1;
    const cls = classNum || (testClassCounters[num] ? testClassCounters[num] : 1);
    const id = `${num}_${cls}`;
    const executeBtn = document.getElementById(`tcExecuteBtn_${id}`);
    const testClassSection = document.getElementById(`testClass_${id}`);
    const fileName = testClassSection ? testClassSection.getAttribute('data-file-name') : `TestFile_${String(cls).padStart(2, '0')}`;

    const folderNameInput = document.getElementById(`generatorFolderName_${num}`);
    const folderName = folderNameInput ? folderNameInput.value.trim() : '';
    const logsContainer = document.getElementById(`classExecutionLogs_${id}`);
    const testClassBody = document.getElementById(`testClassBody_${id}`);

    if (!folderName) {
        alert('Please enter a folder name');
        return;
    }

    if (logsContainer) {
        logsContainer.style.display = 'block';
        logsContainer.innerHTML = '<div style="color: #00d4ff;">⏳ Starting class-level test execution...</div>';
    }
    if (testClassSection) {
        testClassSection.classList.remove('collapsed');
    }

    if (executeBtn) {
        executeBtn.textContent = '⏳ Executing...';
        executeBtn.classList.add('tc-class-execute-disabled');
    }

    try {
        const response = await fetch('/execute-class-tests', {
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
        if (!startResult.success || !startResult.test_id) {
            throw new Error(startResult.message || 'Failed to start class test execution');
        }

        const testId = startResult.test_id;
        const maxPolls = 240; // 4 minutes max for class-level
        let pollCount = 0;
        let result = null;

        while (pollCount < maxPolls) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            pollCount++;

            const statusResponse = await fetch(`/check-test-status/${testId}`);
            const statusResult = await statusResponse.json();

            if (statusResult.status === 'completed') {
                result = statusResult;
                break;
            }
        }

        if (!result) {
            throw new Error('Class test execution timed out');
        }

        if (logsContainer) {
            let logHTML = '<div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">';

            if (result.success) {
                logHTML += '<h4 style="color: #00ff88; margin: 0 0 15px 0;">✅ Class Tests Executed Successfully</h4>';
            } else {
                logHTML += '<h4 style="color: #ff4757; margin: 0 0 15px 0;">❌ Class Tests Failed</h4>';
            }

            if (result.command) {
                logHTML += `<div class="result-item" style="margin-bottom: 10px;"><strong>Command:</strong> <code style="color: #00ff88;">${result.command}</code></div>`;
            }
            if (result.exit_code !== undefined) {
                logHTML += `<div class="result-item" style="margin-bottom: 10px;"><strong>Exit Code:</strong> <code style="color: #00ff88;">${result.exit_code}</code></div>`;
            }
            if (result.message) {
                logHTML += `<div class="result-item" style="margin-bottom: 10px;"><strong>Message:</strong> ${result.message}</div>`;
            }

            let combinedOutput = '';
            if (result.stderr && result.stderr.trim()) {
                combinedOutput = result.stderr;
            }
            if (result.stdout && result.stdout.trim()) {
                combinedOutput += (combinedOutput ? '\n\n' : '') + result.stdout;
            }

            if (combinedOutput) {
                logHTML += '<h4 style="color: #00d4ff; margin-top: 20px; margin-bottom: 10px;">📋 Execution Logs:</h4>';
                logHTML += '<pre style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5; color: #e0e0e0;">' + combinedOutput + '</pre>';
            } else {
                logHTML += '<p style="color: #a0a0a0; margin-top: 20px;">No output captured.</p>';
            }

            logHTML += '</div>';
            logsContainer.innerHTML = logHTML;
        }
    } catch (error) {
        if (logsContainer) {
            logsContainer.innerHTML = '<div style="color: #ff4757;">❌ Failed to execute class tests: ' + error.message + '</div>';
        } else {
            alert('Failed to execute class tests: ' + error.message);
        }
    } finally {
        if (executeBtn) {
            executeBtn.textContent = '▶ Execute Tests';
            executeBtn.classList.remove('tc-class-execute-disabled');
        }
    }
}

async function showAllureReport(compNum, classNum, subNum) {
    const num = compNum || activeTestComponent || 1;
    const cls = classNum || (testClassCounters[num] ? testClassCounters[num] : 1);
    const sub = subNum || (subSectionCounters[`${num}_${cls}`] ? subSectionCounters[`${num}_${cls}`] : 1);
    const id = `${num}_${cls}`;
    const subId = `${id}_${sub}`;
    const reportBtn = document.getElementById(`showReportBtn_${subId}`);
    const statusSection = document.getElementById(`generatorStatus_${subId}`);
    const statusIcon = document.getElementById(`generatorStatusIcon_${subId}`);
    const statusText = document.getElementById(`generatorStatusText_${subId}`);

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
        const outputTabsContainer = document.getElementById(`outputTabsContainer_${subId}`);
        outputTabsContainer.style.display = 'block';
        switchOutputTab(`report-status_${subId}`, num, cls, sub);

        const reportStatusContent = document.getElementById(`reportStatusContent_${subId}`);

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
