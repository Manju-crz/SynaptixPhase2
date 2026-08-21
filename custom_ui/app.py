"""
Flask backend for Custom Test Runner UI
"""

import sys
import os
import threading
import time
import logging
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
from generator_altUtl.file_rename_util import rename_file_in_folder
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


@app.route('/run-test', methods=['POST'])
def run_test():
    """Execute the Swagger UI scraper with provided URL"""
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({'success': False, 'message': 'URL is required'}), 400

    try:
        result = run_swagger_scraper(url)
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
            result = run_openapi_json_parser(spec_url=None, spec_content=spec_content, filename=filename)
            return jsonify(result)
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        spec_url = data.get('url', '')

        if not spec_url:
            return jsonify({'success': False, 'message': 'Spec URL or uploaded JSON file is required'}), 400

        try:
            result = run_openapi_json_parser(spec_url=spec_url)
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
            filename=file_name
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


def execute_test_in_background(test_id, folder_name, file_name, project_root, method_name=None):
    """Background thread function to execute pytest command"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"[Thread {test_id}] Building pytest command...")
        pytest_command = build_pytest_command(folder_name, file_name, method_name=method_name)

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

        # Use the reusable utility to rename the file
        # The utility now handles .py extension automatically
        result = rename_file_in_folder(
            folder_name=folder_name,
            existing_file_name=existing_file_name,
            new_file_name=new_file_name,
            project_root=PROJECT_ROOT,
            search_recursive=True
        )

        # Return the result
        if result['success']:
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


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)