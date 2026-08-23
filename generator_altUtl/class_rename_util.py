"""
Class Rename Utility
Provides reusable functions to rename class names in generated test files.
"""

import os
import re
import logging

logger = logging.getLogger(__name__)


def _is_valid_class_name(name):
    """Check whether a string is a valid Python class identifier."""
    if not name or not isinstance(name, str):
        return False
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name))


def rename_class_in_file(subfolder_name, file_name, old_class_name, new_class_name, project_root=None):
    """
    Rename a class definition in a generated test file.

    Args:
        subfolder_name (str): The subfolder name (e.g., 'TestComponent_01')
        file_name (str): The file name without extension (e.g., 'TestClass_01')
        old_class_name (str): The current class name to be replaced
        new_class_name (str): The new class name
        project_root (str, optional): The project root directory. If None, auto-detects.

    Returns:
        dict: Result dictionary with keys:
            - success (bool): Whether the operation succeeded
            - message (str): Success or error message
            - old_class_name (str): The original class name
            - new_class_name (str): The new class name
            - file_path (str): The path to the modified file

    Example:
        >>> result = rename_class_in_file(
        ...     'TestComponent_01',
        ...     'TestClass_01',
        ...     'TestGeneratedAPIs',
        ...     'TestKeycloakAPIs'
        ... )
        >>> print(result['success'])
        True
    """
    try:
        # Auto-detect project root if not provided
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Validate class names
        if not _is_valid_class_name(old_class_name):
            error_msg = f"Invalid old class name: '{old_class_name}'"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_class_name': old_class_name,
                'new_class_name': new_class_name,
                'file_path': None
            }

        if not _is_valid_class_name(new_class_name):
            error_msg = f"Invalid new class name: '{new_class_name}'"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_class_name': old_class_name,
                'new_class_name': new_class_name,
                'file_path': None
            }

        # Construct the test file path
        test_file_path = os.path.join(project_root, "rest_test", subfolder_name, f"{file_name}.py")

        logger.info(f"Attempting to rename class in file: {test_file_path}")
        logger.info(f"  Old class: {old_class_name}")
        logger.info(f"  New class: {new_class_name}")

        # Check if file exists
        if not os.path.exists(test_file_path):
            error_msg = f"Test file not found: {test_file_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_class_name': old_class_name,
                'new_class_name': new_class_name,
                'file_path': test_file_path
            }

        # Read the file content
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create regex pattern to match class definition
        # Pattern matches: "class old_class_name" at start of a line
        pattern = re.compile(rf'^(\s*class\s+){re.escape(old_class_name)}(\b)', re.MULTILINE)

        # Replace the class name in the class definition (or the first class found)
        if pattern.search(content):
            new_content, count = pattern.subn(rf'\g<1>{new_class_name}\2', content, count=1)
        else:
            # If the UI's old class name doesn't match, rename the first class in the file
            logger.warning(f"Class '{old_class_name}' not found, renaming the first class in the file")
            fallback_pattern = re.compile(r'^(\s*class\s+)(\w+)(\b)', re.MULTILINE)
            new_content, count = fallback_pattern.subn(rf'\g<1>{new_class_name}\3', content, count=1)

        if count == 0:
            error_msg = "No class definition found in file"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_class_name': old_class_name,
                'new_class_name': new_class_name,
                'file_path': test_file_path
            }

        # Write back to file
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        success_msg = f"Successfully renamed class '{old_class_name}' to '{new_class_name}'"
        logger.info(success_msg)

        return {
            'success': True,
            'message': success_msg,
            'old_class_name': old_class_name,
            'new_class_name': new_class_name,
            'file_path': test_file_path
        }

    except Exception as e:
        error_msg = f"Error renaming class: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'success': False,
            'message': error_msg,
            'old_class_name': old_class_name,
            'new_class_name': new_class_name,
            'file_path': None
        }
