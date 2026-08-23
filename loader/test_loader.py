"""
Test Loader Utility
Scans the rest_test directory and returns the existing test structure
(components, files, classes, methods) for the UI Code Generator tab.
"""

import os
import ast
import logging

from loader.prompt_manager import load_prompts, migrate_existing_sidecars, rename_method

logger = logging.getLogger(__name__)


def _parse_test_file(file_path):
    """
    Parse a Python test file and extract the first class name and its methods.

    Args:
        file_path (str): Full path to the .py file.

    Returns:
        tuple: (class_name, list of method names)
    """
    class_name = None
    methods = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            return class_name, methods

        tree = ast.parse(content)

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not child.name.startswith('_'):
                            methods.append(child.name)
                break

    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {e}")
    except Exception as e:
        logger.error(f"Error parsing {file_path}: {e}")

    return class_name, methods


def load_existing_tests(project_root=None):
    """
    Scan the rest_test folder and return the test structure.

    Args:
        project_root (str, optional): Project root directory. If None, it auto-detects.

    Returns:
        dict: {
            'success': bool,
            'components': [
                {
                    'name': component_folder_name,
                    'files': [
                        {
                            'file_name': name_without_py,
                            'class_name': class_name,
                            'methods': [method_name, ...]
                        }
                    ]
                }
            ],
            'message': str
        }
    """
    try:
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        rest_test_dir = os.path.join(project_root, 'rest_test')

        if not os.path.isdir(rest_test_dir):
            return {
                'success': True,
                'components': [],
                'message': 'rest_test directory not found'
            }

        # Consolidate any old per-file prompt sidecars into the single index
        migrate_existing_sidecars(project_root)

        components = []

        for entry in os.listdir(rest_test_dir):
            component_path = os.path.join(rest_test_dir, entry)
            if not os.path.isdir(component_path) or entry.startswith('.') or entry.startswith('__'):
                continue

            files = []
            for file in os.listdir(component_path):
                if not file.endswith('.py') or file == '__init__.py' or file.startswith('.'):
                    continue

                file_path = os.path.join(component_path, file)
                class_name, methods = _parse_test_file(file_path)

                prompt_data = load_prompts(project_root, entry, file[:-3]) or {}
                method_prompts = prompt_data.get('methods', {})

                methods_with_prompts = []
                for method in methods:
                    prompt = method_prompts.get(method)
                    if prompt is None and method.endswith('_ai'):
                        base_method = method[:-3]
                        prompt = method_prompts.get(base_method)
                        if prompt is not None:
                            # Migrate the legacy prompt key to the new _ai name
                            rename_method(project_root, entry, file[:-3], base_method, method)
                    methods_with_prompts.append({'name': method, 'prompt': prompt})

                files.append({
                    'file_name': file[:-3],
                    'class_name': class_name,
                    'methods': methods_with_prompts
                })

            components.append({
                'name': entry,
                'files': files
            })

        return {
            'success': True,
            'components': components,
            'message': f'Loaded {len(components)} component(s)'
        }

    except Exception as e:
        logger.error(f"Error loading existing tests: {e}")
        return {
            'success': False,
            'components': [],
            'message': f'Error loading existing tests: {str(e)}'
        }
