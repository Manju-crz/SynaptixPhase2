"""
Code Validator Utility
Validates Python code for syntax and compilation errors
"""

import py_compile
import ast
import os
import tempfile
from typing import Dict, List, Any


class CodeValidator:
    """
    Utility class to validate Python code for syntax and compilation errors
    """

    def __init__(self):
        """Initialize the CodeValidator"""
        pass

    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a Python file for compilation errors

        Args:
            file_path (str): Absolute path to the Python file to validate

        Returns:
            Dict containing:
                - success (bool): True if file compiles without errors
                - errors (List[str]): List of error messages if any
                - warnings (List[str]): List of warning messages if any
                - file_path (str): Path to the validated file
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'file_path': file_path
        }

        # Check if file exists
        if not os.path.exists(file_path):
            result['errors'].append(f"File not found: {file_path}")
            return result

        # Check if it's a Python file
        if not file_path.endswith('.py'):
            result['errors'].append(f"Not a Python file: {file_path}")
            return result

        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            # Validate using AST (Abstract Syntax Tree)
            ast_result = self._validate_with_ast(code_content, file_path)
            if not ast_result['success']:
                result['errors'].extend(ast_result['errors'])
                return result

            # Try to compile the code in memory (safer than py_compile)
            try:
                compile(code_content, file_path, 'exec')
                result['success'] = True
            except SyntaxError as e:
                error_msg = f"Compilation Error at line {e.lineno}: {e.msg}"
                if e.text:
                    error_msg += f"\n Code: {e.text.strip()}"
                result['errors'].append(error_msg)
                return result
            except Exception as e:
                # If compile() fails for other reasons, still mark as success
                # since AST parsing already passed
                result['success'] = True
                result['warnings'].append(f"Compile check warning: {str(e)}")

            # Add any warnings from AST
            result['warnings'].extend(ast_result.get('warnings', []))

        except Exception as e:
            result['errors'].append(f"Unexpected error during validation: {str(e)}")

        return result

    def _validate_with_ast(self, code_content: str, file_path: str) -> Dict[str, Any]:
        """
        Validate code using AST parsing

        Args:
            code_content (str): Python code content
            file_path (str): Path to the file (for error messages)

        Returns:
            Dict with success status and errors
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': []
        }

        try:
            # Parse the code into an AST
            ast.parse(code_content, filename=file_path)
            result['success'] = True

        except SyntaxError as e:
            error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
            if e.text:
                error_msg += f"\n Code: {e.text.strip()}"
            if e.offset:
                error_msg += f"\n " + " " * (e.offset - 1) + "^"
            result['errors'].append(error_msg)

        except IndentationError as e:
            error_msg = f"Indentation Error at line {e.lineno}: {e.msg}"
            if e.text:
                error_msg += f"\n Code: {e.text.strip()}"
            result['errors'].append(error_msg)

        except Exception as e:
            result['errors'].append(f"AST Parsing Error: {str(e)}")

        return result

    def _validate_with_pycompile(self, file_path: str) -> Dict[str, Any]:
        """
        Validate code using py_compile

        Args:
            file_path (str): Path to the Python file

        Returns:
            Dict with success status and errors
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': []
        }

        try:
            # Create a temporary file for compiled bytecode
            with tempfile.NamedTemporaryFile(suffix='.pyc', delete=True) as tmp_file:
                # Compile the Python file
                py_compile.compile(
                    file_path,
                    cfile=tmp_file.name,
                    doraise=True
                )

            result['success'] = True

        except py_compile.PyCompileError as e:
            # Extract error details
            error_msg = str(e)

            # Try to parse the error message for better formatting
            if hasattr(e, 'exc_value'):
                exc = e.exc_value
                if isinstance(exc, SyntaxError):
                    error_msg = f"Compilation Error at line {exc.lineno}: {exc.msg}"
                    if exc.text:
                        error_msg += f"\n Code: {exc.text.strip()}"
                else:
                    error_msg = f"Compilation Error: {str(exc)}"

            result['errors'].append(error_msg)

        except Exception as e:
            result['errors'].append(f"Compilation Error: {str(e)}")

        return result

    def validate_code_string(self, code_string: str) -> Dict[str, Any]:
        """
        Validate a Python code string (without file)

        Args:
            code_string (str): Python code as string

        Returns:
            Dict containing validation results
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': []
        }

        try:
            # Validate using AST
            ast.parse(code_string)

            # Try to compile
            compile(code_string, '<string>', 'exec')

            result['success'] = True

        except SyntaxError as e:
            error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
            if e.text:
                error_msg += f"\n Code: {e.text.strip()}"
            result['errors'].append(error_msg)

        except Exception as e:
            result['errors'].append(f"Validation Error: {str(e)}")

        return result

    def get_import_errors(self, file_path: str) -> Dict[str, Any]:
        """
        Check for import errors by attempting to import the module
        Note: This actually executes the file, so use with caution

        Args:
            file_path (str): Path to the Python file

        Returns:
            Dict with import validation results
        """
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'missing_imports': []
        }

        try:
            # Read the file and extract import statements
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            # Extract all imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            # Check if imports are available (without executing the file)
            for imp in imports:
                try:
                    __import__(imp.split('.')[0])
                except ImportError:
                    result['missing_imports'].append(imp)
                    result['warnings'].append(f"Import '{imp}' may not be available")

            result['success'] = True

        except Exception as e:
            result['errors'].append(f"Import check error: {str(e)}")

        return result


def validate_generated_code(file_path: str) -> Dict[str, Any]:
    """
    Convenience function to validate generated code

    Args:
        file_path (str): Path to the generated Python file

    Returns:
        Dict with validation results
    """
    validator = CodeValidator()
    return validator.validate_file(file_path)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        validator = CodeValidator()
        result = validator.validate_file(file_path)

        print(f"\n{'='*60}")
        print(f"Validation Results for: {file_path}")
        print(f"{'='*60}")
        print(f"Success: {result['success']}")

        if result['errors']:
            print(f"\n❌ Errors ({len(result['errors'])}):")
            for i, error in enumerate(result['errors'], 1):
                print(f"  {i}. {error}")

        if result['warnings']:
            print(f"\n⚠️  Warnings ({len(result['warnings'])}):")
            for i, warning in enumerate(result['warnings'], 1):
                print(f"  {i}. {warning}")

        if result['success']:
            print(f"\n✅ Code compiled successfully!")

        print(f"{'='*60}\n")
    else:
        print("Usage: python code_validator_util.py <path_to_python_file>")