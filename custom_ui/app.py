"""
Flask backend for Custom Test Runner UI
"""

import sys
import os
import threading
import time
import logging
import shutil
from flask import Flask, render_template, request, jsonify

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_ui.test_runner import run_swagger_scraper, run_openapi_json_parser
from executor_util.executor_util import ApiExecutor
from executor_util.command_builder_util import build_pytest_command
from executor_util.command_executor_util import CommandExecutor
from generator_util.code_generator_util import CodeGenerator
from generator_util.code_validator_util import CodeValidator
from generator_altUtl.method_rename_util import append_to_method_name, validate_method_name
from generator_altUtl.method_remove_util import remove_method_from_file
from generator_altUtl.class_rename_util import rename_class_in_file
from generator_altUtl.file_rename_util import rename_file_in_folder
from generator_altUtl.file_delete_util import delete_test_file, delete_component
from loader.test_loader import load_existing_tests
from loader import prompt_manager as prompt_manager
from nlp.semantic_search_util import SemanticSearchEngine
from generator_aiUtil.test_method_reader_util import TestMethodReader
from generator_aiUtil.ai_code_modifier_util import modify_generated_code_with_ai
from ext_util.parameter_extractor_util import ParameterExtractor

# Store test execution results in memory
test_execution_results = {}

app = Flask(__name__, template_folder='templates', static_folder='static')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_BASE_PATH = os.path.join(PROJECT_ROOT, "Rest_API_Data")


@app.route('/')
def index():
    """Render the main UI page"""
    return render_template('index.html')


@app.route('/get-test-structure', methods=['GET'])
def get_test_structure():
    """Get the test folder structure with files and methods"""
    import os
    import ast
    import re
    
    test_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rest_test')
    structure = []
    
    try:
        # Iterate through folders in rest_test
        for folder_name in sorted(os.listdir(test_folder)):
            folder_path = os.path.join(test_folder, folder_name)
            
            # Skip if not a directory or if it's __pycache__
            if not os.path.isdir(folder_path) or folder_name.startswith('__'):
                continue
            
            folder_data = {
                'name': folder_name,
                'type': 'folder',
                'files': []
            }
            
            # Iterate through Python files in the folder
            for file_name in sorted(os.listdir(folder_path)):
                if file_name.endswith('.py') and not file_name.startswith('__'):
                    file_path = os.path.join(folder_path, file_name)
                    
                    file_data = {
                        'name': file_name,
                        'type': 'file',
                        'methods': []
                    }
                    
                    # Parse the Python file to extract test methods
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                            tree = ast.parse(file_content)
                            
                            # Find all test methods
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    for item in node.body:
                                        if isinstance(item, ast.FunctionDef):
                                            method_name = item.name
                                            if method_name.startswith('test_'):
                                                # Extract docstring if available
                                                docstring = ast.get_docstring(item) or ''
                                                file_data['methods'].append({
                                                    'name': method_name,
                                                    'description': docstring.strip().split('\n')[0] if docstring else ''
                                                })
                    except Exception as e:
                        logger.warning(f"Could not parse {file_path}: {str(e)}")
                    
                    if file_data['methods']:  # Only add file if it has test methods
                        folder_data['files'].append(file_data)
            
            if folder_data['files']:  # Only add folder if it has files with methods
                structure.append(folder_data)
        
        return jsonify({'success': True, 'structure': structure})
    
    except Exception as e:
        logger.error(f"Error getting test structure: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/run-selected-tests', methods=['POST'])
def run_selected_tests():
    """Execute selected test cases using pytest"""
    import subprocess
    import json
    from datetime import datetime
    
    data = request.get_json() or {}
    test_paths = data.get('test_paths', [])
    
    if not test_paths:
        return jsonify({'success': False, 'message': 'No tests selected'}), 400
    
    try:
        # Convert test paths to pytest format
        # Format: TestComponent_02/TestFile_01.py::TestComponent02TestFile01::test_01_create_a_new_pet
        pytest_args = []
        for test_path in test_paths:
            # Extract folder, file, and method
            parts = test_path.split('/')
            if len(parts) == 2:
                folder = parts[0]
                file_and_method = parts[1].split('::')
                if len(file_and_method) == 2:
                    file_name = file_and_method[0]
                    method_name = file_and_method[1]
                    
                    # Construct the full path
                    test_file_path = os.path.join('rest_test', folder, file_name)
                    
                    # Add to pytest args
                    pytest_args.append(f"{test_file_path}::{method_name}")
        
        if not pytest_args:
            return jsonify({'success': False, 'message': 'Invalid test paths'}), 400
        
        logger.info(f"🚀 Running {len(pytest_args)} tests...")
        logger.info(f"Test paths: {pytest_args}")
        
        # Run pytest with JSON report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_report_path = os.path.join('test_reports', f'test_report_{timestamp}.json')
        
        # Create test_reports directory if it doesn't exist
        os.makedirs('test_reports', exist_ok=True)
        
        # Build pytest command with Allure reporting
        pytest_cmd = [
            'pytest',
            '-v',  # Verbose
            '--tb=short',  # Short traceback
            f'--json-report',
            f'--json-report-file={json_report_path}',
            '--json-report-indent=2',
            '--alluredir=allure-results'  # Generate Allure results
        ] + pytest_args
        
        logger.info(f"Executing: {' '.join(pytest_cmd)}")
        
        # Run pytest
        result = subprocess.run(
            pytest_cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        
        # Parse results
        test_results = {
            'total': len(pytest_args),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'error': 0,
            'duration': 0,
            'tests': []
        }
        
        # Try to read JSON report
        if os.path.exists(json_report_path):
            try:
                with open(json_report_path, 'r') as f:
                    report_data = json.load(f)
                    
                    # Extract summary
                    summary = report_data.get('summary', {})
                    test_results['passed'] = summary.get('passed', 0)
                    test_results['failed'] = summary.get('failed', 0)
                    test_results['skipped'] = summary.get('skipped', 0)
                    test_results['error'] = summary.get('error', 0)
                    test_results['duration'] = report_data.get('duration', 0)
                    
                    # Extract individual test results
                    for test in report_data.get('tests', []):
                        test_results['tests'].append({
                            'name': test.get('nodeid', ''),
                            'outcome': test.get('outcome', 'unknown'),
                            'duration': test.get('duration', 0),
                            'message': test.get('call', {}).get('longrepr', '') if test.get('outcome') == 'failed' else ''
                        })
            except Exception as e:
                logger.warning(f"Could not parse JSON report: {str(e)}")
        
        # If JSON report not available, parse stdout
        if not test_results['tests']:
            # Parse pytest output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'PASSED' in line:
                    test_results['passed'] += 1
                elif 'FAILED' in line:
                    test_results['failed'] += 1
                elif 'SKIPPED' in line:
                    test_results['skipped'] += 1
                elif 'ERROR' in line:
                    test_results['error'] += 1
        
        logger.info(f"✅ Test execution completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
        return jsonify({
            'success': True,
            'results': test_results,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode
        })
    
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/run-all-tests', methods=['POST'])
def run_all_tests():
    """Execute all tests in the rest_test directory using pytest"""
    import subprocess
    import json
    from datetime import datetime
    
    try:
        # Run pytest with JSON report on entire rest_test directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_report_path = os.path.join('test_reports', f'test_report_all_{timestamp}.json')
        
        # Create test_reports directory if it doesn't exist
        os.makedirs('test_reports', exist_ok=True)
        
        # Build pytest command with json-report plugin and Allure reporting
        pytest_cmd = [
            'pytest',
            '-v',  # Verbose
            '--tb=short',  # Short traceback
            '--json-report',
            f'--json-report-file={json_report_path}',
            '--alluredir=allure-results',  # Generate Allure results
            'rest_test/'  # Run all tests in rest_test directory
        ]
        
        logger.info(f"🚀 Running all tests in rest_test/ directory...")
        logger.info(f"Executing: {' '.join(pytest_cmd)}")
        
        # Run pytest
        result = subprocess.run(
            pytest_cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        
        # Parse results
        test_results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'error': 0,
            'duration': 0,
            'tests': []
        }
        
        # Try to read JSON report
        if os.path.exists(json_report_path):
            try:
                with open(json_report_path, 'r') as f:
                    report_data = json.load(f)
                    
                    # Extract summary
                    summary = report_data.get('summary', {})
                    test_results['passed'] = summary.get('passed', 0)
                    test_results['failed'] = summary.get('failed', 0)
                    test_results['skipped'] = summary.get('skipped', 0)
                    test_results['error'] = summary.get('error', 0)
                    test_results['duration'] = report_data.get('duration', 0)
                    test_results['total'] = test_results['passed'] + test_results['failed'] + test_results['skipped'] + test_results['error']
                    
                    # Extract individual test results
                    for test in report_data.get('tests', []):
                        test_results['tests'].append({
                            'name': test.get('nodeid', ''),
                            'outcome': test.get('outcome', 'unknown'),
                            'duration': test.get('duration', 0),
                            'message': test.get('call', {}).get('longrepr', '') if test.get('outcome') == 'failed' else ''
                        })
            except Exception as e:
                logger.warning(f"Could not parse JSON report: {str(e)}")
        
        # If JSON report not available, parse stdout
        if not test_results['tests']:
            # Parse pytest output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'PASSED' in line:
                    test_results['passed'] += 1
                elif 'FAILED' in line:
                    test_results['failed'] += 1
                elif 'SKIPPED' in line:
                    test_results['skipped'] += 1
                elif 'ERROR' in line:
                    test_results['error'] += 1
        
        logger.info(f"✅ Test execution completed: {test_results['passed']} passed, {test_results['failed']} failed")
        
        return jsonify({
            'success': True,
            'results': test_results,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode
        })
    
    except Exception as e:
        logger.error(f"Error running all tests: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/run-test', methods=['POST'])
def run_test():
    """Execute the Swagger UI scraper with provided URL"""
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({'success': False, 'message': 'URL is required'}), 400

    try:
        filename_prefix = data.get('filename_prefix', 'Swagger_Data')
        logger.info(f"📝 Received filename_prefix: '{filename_prefix}'")
        logger.info(f"📝 Request data: {data}")
        result = run_swagger_scraper(url, filename_prefix)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/run-json-parser', methods=['POST'])
def run_json_parser():
    """Execute the OpenAPI JSON parser with provided spec URL or uploaded file content"""
    data = request.get_json() or {}
    request_type = data.get('type', 'url')

    if request_type == 'file':
        spec_content = data.get('content', '')
        filename = data.get('filename', 'uploaded_openapi.json')

        if not spec_content:
            return jsonify({'success': False, 'message': 'JSON file content is required'}), 400

        try:
            filename_prefix = data.get('filename_prefix', 'OpenAPI_Data')
            result = run_openapi_json_parser(spec_url=None, spec_content=spec_content, filename=filename, filename_prefix=filename_prefix)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        spec_url = data.get('url', '')

        if not spec_url:
            return jsonify({'success': False, 'message': 'Spec URL or uploaded JSON file is required'}), 400

        try:
            filename_prefix = data.get('filename_prefix', 'OpenAPI_Data')
            logger.info(f"📝 Received filename_prefix: '{filename_prefix}'")
            logger.info(f"📝 Request data: {data}")
            result = run_openapi_json_parser(spec_url=spec_url, filename_prefix=filename_prefix)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/get-excel-files', methods=['GET'])
def get_excel_files():
    """Get list of available Excel files"""
    try:
        print(f"[DEBUG] Checking Excel folder: {EXCEL_BASE_PATH}")

        if not os.path.exists(EXCEL_BASE_PATH):
            print(f"[ERROR] Excel folder not found: {EXCEL_BASE_PATH}")
            return jsonify({'success': False, 'message': 'Excel data folder not found', 'files': []})

        files = []
        all_files = os.listdir(EXCEL_BASE_PATH)
        print(f"[DEBUG] Found {len(all_files)} total files in folder")

        for filename in all_files:
            if filename.endswith('.xlsx'):
                file_path = os.path.join(EXCEL_BASE_PATH, filename)
                file_size = os.path.getsize(file_path) / 1024
                files.append({
                    'name': filename,
                    'path': file_path,
                    'size': f'{file_size:.1f} KB'
                })

        print(f"[DEBUG] Found {len(files)} Excel files")
        files.sort(key=lambda x: x['name'], reverse=True)

        return jsonify({'success': True, 'files': files})
    except Exception as e:
        print(f"[ERROR] Exception in get_excel_files: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e), 'files': []})


@app.route('/run-executor', methods=['POST'])
def run_executor():
    """Execute API calls using natural language queries"""
    data = request.get_json()
    excel_path = data.get('excel_path', '')
    base_url = data.get('base_url', '')
    query = data.get('query', '')

    if not excel_path:
        return jsonify({'success': False, 'message': 'Excel file path is required'}), 400

    if not base_url:
        return jsonify({'success': False, 'message': 'Base URL is required'}), 400

    if not query:
        return jsonify({'success': False, 'message': 'Query is required'}), 400

    try:
        logs = []
        logs.append(f"Excel File: {os.path.basename(excel_path)}")
        logs.append(f"Base URL: {base_url}")
        logs.append(f"Query: {query}")
        logs.append("="*80)

        # Initialize executor
        executor = ApiExecutor(
            excel_path=excel_path,
            base_url=base_url
        )

        # Check if multiple queries (separated by semicolon)
        queries = [q.strip() for q in query.split(';') if q.strip()]
        logs.append(f"Total Queries: {len(queries)}")
        logs.append("="*80)

        results = []
        for i, q in enumerate(queries, 1):
            logs.append(f"\nExecuting Query {i}/{len(queries)}: {q}")
            result = executor.execute_api_call(q)
            results.append(result)

            if result['success']:
                logs.append(f"✅ Success - Sl_No: {result.get('sl_no')}, Status: {result.get('status_code')}")
            else:
                logs.append(f"❌ Failed - Error: {result.get('error')}")

        executor.close()

        logs.append("="*80)
        logs.append(f"Execution Summary: {sum(1 for r in results if r['success'])}/{len(results)} successful")

        return jsonify({
            'success': True,
            'results': results,
            'logs': logs,
            'total_queries': len(queries),
            'successful': sum(1 for r in results if r['success']),
            'failed': sum(1 for r in results if not r['success'])
        })

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return jsonify({
            'success': False,
            'message': str(e),
            'logs': [error_trace]
        }), 500


@app.route('/run-generator', methods=['POST'])
def run_generator():
    """Generate pytest test code from natural language queries"""
    data = request.get_json()
    excel_path = data.get('excel_path', '')
    base_url = data.get('base_url', '')
    folder_name = data.get('folder_name', '')
    file_name = data.get('file_name', '')
    query = data.get('query', '')
    ai_model = data.get('ai_model', 'openai')
    replace_method = data.get('replace_method', False)
    method_name = data.get('method_name')

    if not excel_path:
        return jsonify({'success': False, 'message': 'Excel file path is required'}), 400

    if not base_url:
        return jsonify({'success': False, 'message': 'Base URL is required'}), 400

    if not folder_name:
        return jsonify({'success': False, 'message': 'Folder name is required'}), 400

    if not file_name:
        return jsonify({'success': False, 'message': 'File name is required'}), 400

    if not query:
        return jsonify({'success': False, 'message': 'Query is required'}), 400

    try:
        logs = []
        logs.append(f"Excel File: {os.path.basename(excel_path)}")
        logs.append(f"Base URL: {base_url}")
        logs.append(f"Folder Name: {folder_name}")
        logs.append(f"File Name: {file_name}.py")
        logs.append(f"Query: {query}")
        logs.append("="*80)

        # Parse queries (separated by semicolon)
        queries = [q.strip() for q in query.split(';') if q.strip()]
        logs.append(f"Total Queries: {len(queries)}")
        logs.append("="*80)

        # Use semantic search to find Sl_Nos for each query
        # Use same search columns as Executor for consistency
        search_columns = ['Component', 'Component_SmallDescription', 'Operation_Method',
                           'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary']
        search_engine = SemanticSearchEngine(excel_path, search_columns=search_columns)
        sl_nos = []

        for i, q in enumerate(queries, 1):
            # Extract only the first statement (before -> or →) for searching
            if '->' in q:
                search_query = q.split('->')[0].strip()
            elif '→' in q:
                search_query = q.split('→')[0].strip()
            else:
                search_query = q
            
            logs.append(f"\nSearching for query {i}/{len(queries)}: {search_query}")
            if search_query != q:
                logs.append(f"   Full query with instructions: {q}")
            
            sl_no = search_engine.get_best_match_sl_no(search_query)
            if sl_no:
                sl_nos.append(sl_no)
                logs.append(f"✅ Found Sl_No: {sl_no}")
            else:
                logs.append(f"❌ No match found for: {search_query}")

        if not sl_nos:
            return jsonify({
                'success': False,
                'message': 'No matching APIs found for the queries',
                'logs': logs
            })

        # Generate test file
        logs.append("\n" + "="*80)
        logs.append("Generating test code...")
        logs.append("="*80)

        generator = CodeGenerator(excel_path=excel_path, base_url=base_url)
        result = generator.generate_test_file(
            sl_nos=sl_nos,
            queries=queries,
            folder_name=folder_name,
            filename=file_name,
            original_query=query,
            replace_method_name=method_name if replace_method and method_name else None
        )

        if result['success']:
            logs.append(f"\n✅ Test file generated successfully!")
            logs.append(f"   Location: {result['file_path']}")
            logs.append(f"   Tests: {result['tests_generated']}")

            # Read generated test methods code
            try:
                logs.append(f"\n📄 Reading generated test methods...")
                reader = TestMethodReader(result['file_path'])

                # Use only the newly generated method names (not all methods in the file)
                # so that appending to an existing file doesn't re-read old methods
                new_method_names = result.get('generated_method_names', [])
                if new_method_names:
                    all_methods = new_method_names
                    logs.append(f"   Newly generated methods: {new_method_names}")
                else:
                    all_methods = reader.get_all_test_methods()

                generated_code = []
                for method_name in all_methods:
                    method_result = reader.read_test_method(method_name)
                    if method_result['success']:
                        generated_code.append({
                            'method_name': method_name,
                            'code': method_result['code'],
                            'line_count': method_result['line_count'],
                            'step_count': method_result['step_count']
                        })
                        logs.append(f"   ✅ Read method: {method_name} ({method_result['step_count']} steps)")

                result['generated_code'] = generated_code
                logs.append(f"   Total methods read: {len(generated_code)}")

                # AI Code Modification - if queries have instructions
                has_instructions = any('->' in q or '→' in q for q in queries)
                if has_instructions and all_methods:
                    logs.append(f"\n🤖 AI Code Modification...")
                    logs.append(f"   AI Model: {ai_model}")
                    logs.append(f"   Detected instructions in queries")

                    try:
                        # Extract Excel data for each Sl_No
                        extractor = ParameterExtractor(excel_path)
                        excel_data = []
                        for sl_no in sl_nos:
                            data = extractor.extract_parameters(sl_no)
                            excel_data.append(data)

                        # Modify code with AI (using selected model)
                        original_method_name = all_methods[0]
                        original_code = generated_code[0]['code']

                        ai_result = modify_generated_code_with_ai(
                            file_path=result['file_path'],
                            method_name=original_method_name,
                            original_code=original_code,
                            excel_data=excel_data,
                            queries=queries,
                            ai_provider=ai_model,
                            replace_original=True  # Replace original method with AI version
                        )

                        if ai_result['success']:
                            if ai_result.get('replaced'):
                                logs.append(f"   ✅ Original method replaced with AI version: {ai_result['new_method_name']}")
                            else:
                                logs.append(f"   ✅ AI-modified method created: {ai_result['new_method_name']}")
                            logs.append(f"   Instructions applied: {ai_result['instructions_applied']}")

                            # Sync prompt sidecar with the new AI method name
                            if ai_result['new_method_name'] != original_method_name:
                                prompt_manager.rename_method(
                                    PROJECT_ROOT, folder_name, file_name,
                                    original_method_name, ai_result['new_method_name']
                                )

                            # Read the AI-modified method
                            reader_ai = TestMethodReader(result['file_path'])
                            ai_method_result = reader_ai.read_test_method(ai_result['new_method_name'])

                            if ai_method_result['success']:
                                # Add AI method to generated_code list (keep both for UI display)
                                generated_code.append({
                                    'method_name': ai_result['new_method_name'],
                                    'code': ai_method_result['code'],
                                    'line_count': ai_method_result['line_count'],
                                    'step_count': ai_method_result['step_count'],
                                    'ai_modified': True
                                })
                                result['generated_code'] = generated_code
                                logs.append(f"   ✅ AI-modified code added to results")
                                logs.append(f"   📝 Note: File contains only AI method, UI shows both for reference")
                        else:
                            logs.append(f"   ⚠️ AI modification failed: {ai_result.get('error')}")

                    except Exception as ai_error:
                        logs.append(f"   ⚠️ AI modification error: {str(ai_error)}")

            except Exception as e:
                logs.append(f"   ⚠️ Could not read generated code: {str(e)}")
                result['generated_code'] = []

            # Validate generated code for compilation errors (ALWAYS RUN)
            logs.append(f"\n🔍 Validating generated code...")
            try:
                validator = CodeValidator()
                validation_result = validator.validate_file(result['file_path'])

                if validation_result['success']:
                    logs.append(f"   ✅ Code validation passed - No compilation errors!")
                    result['validation'] = {
                        'success': True,
                        'message': 'Code compiled successfully'
                    }
                else:
                    logs.append(f"   ❌ Code validation failed - Compilation errors found!")
                    for i, error in enumerate(validation_result['errors'], 1):
                        logs.append(f"   Error {i}: {error}")
                    result['validation'] = {
                        'success': False,
                        'errors': validation_result['errors']
                    }

                # Check for warnings
                if validation_result.get('warnings'):
                    logs.append(f"\n⚠️ Validation Warnings:")
                    for i, warning in enumerate(validation_result['warnings'], 1):
                        logs.append(f"   Warning {i}: {warning}")

            except Exception as validation_error:
                logs.append(f"   ⚠️ Validation error: {str(validation_error)}")
                result['validation'] = {
                    'success': False,
                    'errors': [str(validation_error)]
                }
        else:
            logs.append(f"\n❌ Failed to generate test file")
            logs.append(f"   Error: {result.get('error')}")

        result['logs'] = logs
        return jsonify(result)

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return jsonify({
            'success': False,
            'message': str(e),
            'logs': [error_trace]
        }), 500


def execute_test_in_background(test_id, folder_name, file_name, project_root, method_name=None, class_only=False):
    """Background thread function to execute pytest command"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"[Thread {test_id}] Building pytest command...")
        pytest_command = build_pytest_command(folder_name, file_name, method_name=method_name, class_only=class_only)

        if not pytest_command:
            test_execution_results[test_id] = {
                'success': False,
                'message': f'Failed to build pytest command for {folder_name}/{file_name}.py',
                'command': '',
                'exit_code': -1,
                'stdout': '',
                'stderr': '',
                'status': 'completed'
            }
            return

        logger.info(f"[Thread {test_id}] Executing: {pytest_command}")
        executor = CommandExecutor(working_directory=project_root)
        result = executor.execute_pytest_command(pytest_command, timeout=300)

        result['status'] = 'completed'
        test_execution_results[test_id] = result
        logger.info(f"[Thread {test_id}] Execution completed - success: {result.get('success')}")

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"[Thread {test_id}] Error: {str(e)}")
        test_execution_results[test_id] = {
            'success': False,
            'message': str(e),
            'error': error_trace,
            'command': '',
            'exit_code': -1,
            'stdout': '',
            'stderr': '',
            'status': 'completed'
        }


@app.route('/execute-generated-test', methods=['POST'])
def execute_generated_test():
    """
    Start test execution in background thread and return immediately
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.info("=== Execute Generated Test Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')
        method_name = data.get('method_name')

        logger.info(f"Received from UI - folder: {folder_name}, file: {file_name}, method: {method_name}")

        if not folder_name or not file_name:
            logger.error("Missing folder_name or file_name from UI")
            return jsonify({
                'success': False,
                'message': 'Folder name and file name are required.',
                'status': 'error'
            }), 400

        # Generate unique test ID
        test_id = f"{folder_name}_{file_name}_{int(time.time())}"

        # Initialize result as running
        test_execution_results[test_id] = {
            'status': 'running',
            'message': 'Test execution started...'
        }

        # Start execution in background thread
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        thread = threading.Thread(
            target=execute_test_in_background,
            args=(test_id, folder_name, file_name, project_root, method_name),
            daemon=True
        )
        thread.start()

        logger.info(f"Started background thread for test_id: {test_id}")

        # Return test_id for polling
        return jsonify({
            'success': True,
            'test_id': test_id,
            'status': 'running',
            'message': 'Test execution started in background'
        })

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error starting test execution: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e),
            'error': error_trace,
            'status': 'error'
        }), 500


@app.route('/execute-class-tests', methods=['POST'])
def execute_class_tests():
    """Start class-level test execution in background thread and return immediately"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.info("=== Execute Class Tests Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')

        logger.info(f"Received from UI - folder: {folder_name}, file: {file_name}")

        if not folder_name or not file_name:
            logger.error("Missing folder_name or file_name from UI")
            return jsonify({
                'success': False,
                'message': 'Folder name and file name are required.',
                'status': 'error'
            }), 400

        # Generate unique test ID
        test_id = f"{folder_name}_{file_name}_class_{int(time.time())}"

        # Initialize result as running
        test_execution_results[test_id] = {
            'status': 'running',
            'message': 'Class test execution started...'
        }

        # Start execution in background thread
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        thread = threading.Thread(
            target=execute_test_in_background,
            args=(test_id, folder_name, file_name, project_root),
            kwargs={'class_only': True},
            daemon=True
        )
        thread.start()

        logger.info(f"Started background thread for test_id: {test_id}")

        # Return test_id for polling
        return jsonify({
            'success': True,
            'test_id': test_id,
            'status': 'running',
            'message': 'Class test execution started in background'
        })

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error starting class test execution: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e),
            'error': error_trace,
            'status': 'error'
        }), 500


@app.route('/check-test-status/<test_id>', methods=['GET'])
def check_test_status(test_id):
    """Check the status of a running test"""
    if test_id not in test_execution_results:
        return jsonify({
            'success': False,
            'message': 'Test ID not found',
            'status': 'not_found'
        }), 404

    result = test_execution_results[test_id]
    return jsonify(result)


@app.route('/rename-method', methods=['POST'])
def rename_method():
    """Rename a test method in the generated test file by appending text"""
    try:
        logger.info("=== Rename Method Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')
        old_method_name = data.get('old_method_name')
        append_text = data.get('append_text')

        logger.info(f"Received - folder: {folder_name}, file: {file_name}, old_method: {old_method_name}, append: {append_text}")

        if not all([folder_name, file_name, old_method_name, append_text]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters'
            }), 400

        # Validate the append text
        new_method_name = f"{old_method_name}_{append_text}"
        is_valid, error_msg = validate_method_name(new_method_name)
        if not is_valid:
            logger.error(f"Invalid method name: {error_msg}")
            return jsonify({
                'success': False,
                'message': f'Invalid method name: {error_msg}'
            }), 400

        # Use the reusable utility to append to method name
        result = append_to_method_name(
            subfolder_name=folder_name,
            file_name=file_name,
            old_method_name=old_method_name,
            append_text=append_text,
            delimiter='_',
            project_root=PROJECT_ROOT
        )

        # Return the result
        if result['success']:
            prompt_manager.rename_method(PROJECT_ROOT, folder_name, file_name, old_method_name, result['new_method_name'])
            return jsonify({
                'success': True,
                'message': result['message'],
                'new_method_name': result['new_method_name']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 404

    except Exception as e:
        logger.error(f"Error renaming method: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/delete-method', methods=['POST'])
def delete_method():
    """Delete a test method from the generated test file"""
    try:
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')
        method_name = data.get('method_name')

        logger.info(f"Received - folder: {folder_name}, file: {file_name}, method: {method_name}")

        if not all([folder_name, file_name, method_name]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters'
            }), 400

        # Use the reusable utility to remove the method
        result = remove_method_from_file(
            subfolder_name=folder_name,
            file_name=file_name,
            method_name=method_name,
            project_root=PROJECT_ROOT
        )

        # Return the result
        if result['success']:
            prompt_manager.delete_method(PROJECT_ROOT, folder_name, file_name, method_name)
            return jsonify(result)
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"Error deleting method: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/rename-file', methods=['POST'])
def rename_file():
    """Rename a test file in the specified folder"""
    try:
        logger.info("=== Rename File Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')
        existing_file_name = data.get('existing_file_name')
        new_file_name = data.get('new_file_name')

        logger.info(f"Received - folder: {folder_name}, existing_file: {existing_file_name}, new_file: {new_file_name}")

        if not all([folder_name, existing_file_name, new_file_name]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters (folder_name, existing_file_name, new_file_name)'
            }), 400

        # Use the reusable utility to rename the file directly under rest_test/
        result = rename_file_in_folder(
            folder_name=folder_name,
            existing_file_name=existing_file_name,
            new_file_name=new_file_name,
            project_root=os.path.join(PROJECT_ROOT, 'rest_test'),
            search_recursive=False
        )

        # Return the result
        if result['success']:
            prompt_manager.rename_file(PROJECT_ROOT, folder_name, existing_file_name, new_file_name)
            return jsonify({
                'success': True,
                'message': result['message'],
                'old_file_name': result['old_file_name'],
                'new_file_name': result['new_file_name'],
                'old_file_path': result['old_file_path'],
                'new_file_path': result['new_file_path']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 404

    except Exception as e:
        logger.error(f"Error renaming file: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/delete-file', methods=['POST'])
def delete_file():
    """Delete a test file in the specified folder"""
    try:
        logger.info("=== Delete File Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')

        logger.info(f"Received - folder: {folder_name}, file: {file_name}")

        if not all([folder_name, file_name]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters (folder_name, file_name)'
            }), 400

        # Use the reusable utility to delete the file
        result = delete_test_file(
            subfolder_name=folder_name,
            file_name=file_name,
            project_root=PROJECT_ROOT
        )

        # Return the result
        if result['success']:
            prompt_manager.delete_file(PROJECT_ROOT, folder_name, file_name)
            return jsonify({
                'success': True,
                'message': result['message'],
                'file_path': result['file_path']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 404

    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/rename-class', methods=['POST'])
def rename_class():
    """Rename a class inside a generated test file"""
    try:
        logger.info("=== Rename Class Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')
        old_class_name = data.get('old_class_name')
        new_class_name = data.get('new_class_name')

        logger.info(f"Received - folder: {folder_name}, file: {file_name}, old_class: {old_class_name}, new_class: {new_class_name}")

        if not all([folder_name, file_name, old_class_name, new_class_name]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters (folder_name, file_name, old_class_name, new_class_name)'
            }), 400

        # Use the reusable utility to rename the class
        result = rename_class_in_file(
            subfolder_name=folder_name,
            file_name=file_name,
            old_class_name=old_class_name,
            new_class_name=new_class_name,
            project_root=PROJECT_ROOT
        )

        # Return the result
        if result['success']:
            prompt_manager.rename_class(PROJECT_ROOT, folder_name, file_name, new_class_name)
            return jsonify({
                'success': True,
                'message': result['message'],
                'file_path': result['file_path'],
                'old_class_name': result['old_class_name'],
                'new_class_name': result['new_class_name']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 404

    except Exception as e:
        logger.error(f"Error renaming class: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/rename-component', methods=['POST'])
def rename_component_folder():
    """Rename a component folder in rest_test"""
    try:
        logger.info("=== Rename Component Route Called ===")
        data = request.get_json()
        old_folder_name = data.get('old_folder_name')
        new_folder_name = data.get('new_folder_name')

        logger.info(f"Received - old: {old_folder_name}, new: {new_folder_name}")

        if not old_folder_name or not new_folder_name:
            return jsonify({
                'success': False,
                'message': 'Missing required parameters: old_folder_name and new_folder_name'
            }), 400

        old_path = os.path.join(PROJECT_ROOT, 'rest_test', old_folder_name)
        new_path = os.path.join(PROJECT_ROOT, 'rest_test', new_folder_name)

        if os.path.isdir(new_path):
            return jsonify({
                'success': False,
                'message': f'Component folder "{new_folder_name}" already exists'
            }), 409

        if os.path.isdir(old_path):
            try:
                os.rename(old_path, new_path)
                logger.info(f"Renamed component folder: {old_folder_name} -> {new_folder_name}")
            except Exception as e:
                logger.error(f"Failed to rename component folder: {e}")
                return jsonify({
                    'success': False,
                    'message': f'Failed to rename component folder: {str(e)}'
                }), 500
        else:
            logger.info(f"Component folder does not exist yet; updating name only")

        # Sync the prompt index
        prompt_manager.rename_component(PROJECT_ROOT, old_folder_name, new_folder_name)

        return jsonify({
            'success': True,
            'message': f'Component folder renamed to "{new_folder_name}"',
            'old_folder_name': old_folder_name,
            'new_folder_name': new_folder_name
        })

    except Exception as e:
        logger.error(f"Error renaming component: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/delete-component', methods=['POST'])
def delete_component_folder():
    """Delete a complete component folder from rest_test"""
    try:
        logger.info("=== Delete Component Route Called ===")
        data = request.get_json()
        folder_name = data.get('folder_name')

        logger.info(f"Received - folder: {folder_name}")

        if not folder_name:
            return jsonify({
                'success': False,
                'message': 'Missing required parameter: folder_name'
            }), 400

        # Use the reusable utility to delete the component folder
        result = delete_component(
            subfolder_name=folder_name,
            project_root=PROJECT_ROOT
        )

        # Return the result
        if result['success']:
            prompt_manager.delete_component(PROJECT_ROOT, folder_name)
            return jsonify({
                'success': True,
                'message': result['message'],
                'folder_path': result['folder_path']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 404

    except Exception as e:
        logger.error(f"Error deleting component: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/clear-execution-results', methods=['POST'])
def clear_execution_results():
    """Delete allure-results and allure-report folders"""
    try:
        logger.info("=== Clear Execution Results Route Called ===")
        results_path = os.path.join(PROJECT_ROOT, "allure-results")
        report_path = os.path.join(PROJECT_ROOT, "allure-report")
        deleted = []
        for path in (results_path, report_path):
            if os.path.exists(path):
                shutil.rmtree(path)
                deleted.append(os.path.basename(path))
        return jsonify({
            'success': True,
            'message': f"Deleted: {', '.join(deleted)}" if deleted else "Nothing to clear",
            'deleted': deleted
        })
    except Exception as e:
        logger.error(f"Error clearing execution results: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/show-allure-report', methods=['POST'])
def show_allure_report():
    """Generate Allure report and return URL to open in same browser"""
    import logging
    import shutil
    logger = logging.getLogger(__name__)

    try:
        logger.info("=== Show Allure Report Route Called ===")

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        allure_results_path = os.path.join(project_root, "allure-results")
        allure_report_path = os.path.join(project_root, "allure-report")

        # Check if allure-results directory exists
        if not os.path.exists(allure_results_path):
            logger.error(f"Allure results directory not found: {allure_results_path}")
            return jsonify({
                'success': False,
                'message': 'Allure results directory not found. Please run tests first.'
            }), 404

        # Check if there are any results
        result_files = [f for f in os.listdir(allure_results_path) if f.endswith('.json') or f.endswith('.txt')]
        if not result_files:
            logger.error("No test results found in allure-results directory")
            return jsonify({
                'success': False,
                'message': 'No test results found. Please run tests first.'
            }), 404

        logger.info(f"Generating Allure report from: {allure_results_path}")

        # Remove old report if exists
        if os.path.exists(allure_report_path):
            logger.info(f"Removing old report: {allure_report_path}")
            shutil.rmtree(allure_report_path)

        # Initialize executor
        executor = CommandExecutor(working_directory=project_root)
        
        # Check if allure CLI is installed
        check_allure = executor.execute_command('allure --version', timeout=5)
        
        if not check_allure['success']:
            # Allure CLI not installed - provide helpful error message
            logger.error("Allure CLI not found")
            return jsonify({
                'success': False,
                'message': 'Allure CLI is not installed. Please install it using: scoop install allure (or download from https://github.com/allure-framework/allure2/releases)',
                'stderr': 'Allure command-line tool not found in PATH'
            }), 500
        
        # Generate Allure report using 'allure generate'
        command = f'allure generate "{allure_results_path}" -o "{allure_report_path}" --clean'
        logger.info(f"Executing command: {command}")

        result = executor.execute_command(command, timeout=60)

        if not result['success']:
            logger.error(f"Failed to generate Allure report: {result.get('message')}")
            return jsonify({
                'success': False,
                'message': f"Failed to generate Allure report: {result.get('message')}",
                'stderr': result.get('stderr', '')
            }), 500

        logger.info("Allure report generated successfully")

        # Return URL to open in same browser
        report_url = '/allure-report/index.html'

        return jsonify({
            'success': True,
            'message': 'Allure report generated successfully',
            'url': report_url
        })

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error generating Allure report: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to generate Allure report: {str(e)}',
            'error': error_trace
        }), 500


@app.route('/allure-report/<path:filename>')
def serve_allure_report(filename):
    """Serve Allure report files"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    allure_report_path = os.path.join(project_root, "allure-report")

    from flask import send_from_directory
    return send_from_directory(allure_report_path, filename)


@app.route('/load-existing-tests', methods=['GET'])
def load_existing_tests_route():
    """Return the existing test structure from the rest_test folder"""
    try:
        result = load_existing_tests(project_root=PROJECT_ROOT)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in /load-existing-tests: {str(e)}")
        return jsonify({
            'success': False,
            'components': [],
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/update-prompt', methods=['POST'])
def update_prompt_route():
    """Update the stored prompt for a method in the sidecar file"""
    try:
        data = request.get_json()
        folder_name = data.get('folder_name')
        file_name = data.get('file_name')
        class_name = data.get('class_name')
        method_name = data.get('method_name')
        prompt = data.get('prompt', '')

        if not all([folder_name, file_name, method_name, prompt is not None]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters (folder_name, file_name, method_name, prompt)'
            }), 400

        prompt_manager.update_prompt(PROJECT_ROOT, folder_name, file_name, class_name, method_name, prompt)

        return jsonify({
            'success': True,
            'message': 'Prompt updated successfully'
        })

    except Exception as e:
        logger.error(f"Error updating prompt: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)