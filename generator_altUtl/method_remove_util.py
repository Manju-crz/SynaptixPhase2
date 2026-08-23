"""
Method Remove Utility
Provides reusable functions to remove/clear test methods from generated test files.
"""

import os
import ast
import re
import logging

logger = logging.getLogger(__name__)


def remove_method_from_file(subfolder_name, file_name, method_name, project_root=None):
    """
    Remove a specific test method from a generated test file.

    Args:
        subfolder_name (str): The subfolder name (e.g., 'TestComponent_01')
        file_name (str): The file name without extension (e.g., 'TestClass_01')
        method_name (str): The method name to remove (e.g., 'test_01_example')
        project_root (str, optional): The project root directory. If None, auto-detects.

    Returns:
        dict: Result dictionary with keys:
            - success (bool): Whether the operation succeeded
            - message (str): Success or error message
            - method_name (str): The removed method name
            - file_path (str): The path to the modified file
            - removed_lines (int): Number of lines removed (0 if not found)

    Example:
        >>> result = remove_method_from_file(
        ...     'TestComponent_01',
        ...     'TestClass_01',
        ...     'test_01_example'
        ... )
        >>> print(result['success'])
        True
    """
    try:
        # Auto-detect project root if not provided
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Construct the test file path
        test_file_path = os.path.join(project_root, "rest_test", subfolder_name, f"{file_name}.py")

        logger.info(f"Attempting to remove method from file: {test_file_path}")
        logger.info(f"  Method: {method_name}")

        # Check if file exists
        if not os.path.exists(test_file_path):
            error_msg = f"Test file not found: {test_file_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'method_name': method_name,
                'file_path': test_file_path,
                'removed_lines': 0
            }

        # Read the file content while preserving line endings
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines(keepends=True)

        if not lines:
            error_msg = "Test file is empty"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'method_name': method_name,
                'file_path': test_file_path,
                'removed_lines': 0
            }

        # Try to parse the file with AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            error_msg = f"Failed to parse file due to syntax error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'method_name': method_name,
                'file_path': test_file_path,
                'removed_lines': 0
            }

        # Find all FunctionDef nodes matching the method name
        matching_nodes = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name
        ]

        if not matching_nodes:
            error_msg = f"Method '{method_name}' not found in file"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'method_name': method_name,
                'file_path': test_file_path,
                'removed_lines': 0
            }

        # Pick the first matching method (earliest in file)
        target_node = min(matching_nodes, key=lambda n: n.lineno)

        # Determine start line (include decorators if present)
        if target_node.decorator_list:
            start_line = min(dec.lineno for dec in target_node.decorator_list)
        else:
            start_line = target_node.lineno

        # Determine end line
        end_line = getattr(target_node, 'end_lineno', None)
        if end_line is None:
            # Fallback for very old Python versions: search for next method/class at same or lower indentation
            end_line = _fallback_find_end_line(lines, start_line)

        # Convert 1-indexed line numbers to 0-indexed list slicing
        removed_lines_count = end_line - start_line + 1
        new_lines = lines[:start_line - 1] + lines[end_line:]

        # Write the updated content back
        new_content = ''.join(new_lines)
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        success_msg = f"Successfully removed method '{method_name}' ({removed_lines_count} lines)"
        logger.info(success_msg)

        return {
            'success': True,
            'message': success_msg,
            'method_name': method_name,
            'file_path': test_file_path,
            'removed_lines': removed_lines_count
        }

    except Exception as e:
        error_msg = f"Error removing method: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'success': False,
            'message': error_msg,
            'method_name': method_name,
            'file_path': test_file_path if 'test_file_path' in locals() else 'unknown',
            'removed_lines': 0
        }


def clear_method_from_file(subfolder_name, file_name, method_name, project_root=None):
    """
    Alias for remove_method_from_file.

    Clears/removes a test method from a generated test file.
    """
    return remove_method_from_file(subfolder_name, file_name, method_name, project_root)


def _fallback_find_end_line(lines, start_line):
    """
    Fallback method to find the end line of a method if end_lineno is not available.
    Looks for the next line that is not more indented than the method definition.
    """
    if start_line < 1 or start_line > len(lines):
        return len(lines)

    # Get the indentation of the method definition line
    def_line = lines[start_line - 1]
    base_indent_match = re.match(r'^(\s*)', def_line)
    base_indent = base_indent_match.group(1) if base_indent_match else ''
    base_indent_len = len(base_indent)

    for i in range(start_line, len(lines)):
        line = lines[i]
        stripped = line.lstrip()

        # Skip empty lines
        if not stripped:
            continue

        # Find the next line that is not more indented than the method definition
        current_indent = len(line) - len(stripped)
        if current_indent <= base_indent_len:
            return i

    return len(lines)


if __name__ == "__main__":
    # Example usage and testing
    logging.basicConfig(level=logging.INFO)

    print("Method Remove Utility - Example Usage")
    print("=" * 60)

    # Example 1: Remove method
    print("\nExample 1: Remove a method")
    result = remove_method_from_file(
        subfolder_name='TestComponent_01',
        file_name='TestClass_01',
        method_name='test_01_example'
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Removed lines: {result['removed_lines']}")
