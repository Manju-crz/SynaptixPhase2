"""
Method Rename Utility
Provides reusable functions to rename test methods in generated test files.
"""

import os
import re
import logging

logger = logging.getLogger(__name__)


def rename_method_in_file(subfolder_name, file_name, old_method_name, new_method_name, project_root=None):
    """
    Rename a test method in a generated test file.
    
    Args:
        subfolder_name (str): The subfolder name (e.g., 'TestComponent_01')
        file_name (str): The file name without extension (e.g., 'TestClass_01')
        old_method_name (str): The current method name to be replaced
        new_method_name (str): The new method name
        project_root (str, optional): The project root directory. If None, auto-detects.
    
    Returns:
        dict: Result dictionary with keys:
            - success (bool): Whether the operation succeeded
            - message (str): Success or error message
            - old_method_name (str): The original method name
            - new_method_name (str): The new method name
            - file_path (str): The path to the modified file
    
    Example:
        >>> result = rename_method_in_file(
        ...     'TestComponent_01',
        ...     'TestClass_01',
        ...     'test_01_create_pet_ai',
        ...     'test_01_create_pet_ai_updated'
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
        
        logger.info(f"Attempting to rename method in file: {test_file_path}")
        logger.info(f"  Old method: {old_method_name}")
        logger.info(f"  New method: {new_method_name}")
        
        # Check if file exists
        if not os.path.exists(test_file_path):
            error_msg = f"Test file not found: {test_file_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_method_name': old_method_name,
                'new_method_name': new_method_name,
                'file_path': test_file_path
            }
        
        # Read the file content
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create regex pattern to match method definition
        # Pattern matches: "def old_method_name(" with optional whitespace
        pattern = rf'(\s+def\s+){re.escape(old_method_name)}(\s*\()'
        
        # Check if the method exists
        if not re.search(pattern, content):
            error_msg = f"Method '{old_method_name}' not found in file"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_method_name': old_method_name,
                'new_method_name': new_method_name,
                'file_path': test_file_path
            }
        
        # Replace the method name
        new_content = re.sub(pattern, rf'\1{new_method_name}\2', content)
        
        # Verify that replacement occurred
        if content == new_content:
            error_msg = "No changes made to file (replacement failed)"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_method_name': old_method_name,
                'new_method_name': new_method_name,
                'file_path': test_file_path
            }
        
        # Write back to file
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        success_msg = f"Successfully renamed '{old_method_name}' to '{new_method_name}'"
        logger.info(success_msg)
        
        return {
            'success': True,
            'message': success_msg,
            'old_method_name': old_method_name,
            'new_method_name': new_method_name,
            'file_path': test_file_path
        }
    
    except Exception as e:
        error_msg = f"Error renaming method: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'success': False,
            'message': error_msg,
            'old_method_name': old_method_name,
            'new_method_name': new_method_name,
            'file_path': test_file_path if 'test_file_path' in locals() else 'unknown'
        }


def append_to_method_name(subfolder_name, file_name, old_method_name, append_text, delimiter='_', project_root=None):
    """
    Append text to an existing method name using a delimiter.
    
    Args:
        subfolder_name (str): The subfolder name (e.g., 'TestComponent_01')
        file_name (str): The file name without extension (e.g., 'TestClass_01')
        old_method_name (str): The current method name
        append_text (str): The text to append to the method name
        delimiter (str, optional): The delimiter to use between old name and append text. Defaults to '_'.
        project_root (str, optional): The project root directory. If None, auto-detects.
    
    Returns:
        dict: Result dictionary (same format as rename_method_in_file)
    
    Example:
        >>> result = append_to_method_name(
        ...     'TestComponent_01',
        ...     'TestClass_01',
        ...     'test_01_create_pet_ai',
        ...     'updated'
        ... )
        >>> print(result['new_method_name'])
        'test_01_create_pet_ai_updated'
    """
    # Construct the new method name
    new_method_name = f"{old_method_name}{delimiter}{append_text}"
    
    logger.info(f"Appending '{append_text}' to method '{old_method_name}' with delimiter '{delimiter}'")
    
    # Use the rename_method_in_file function
    return rename_method_in_file(
        subfolder_name=subfolder_name,
        file_name=file_name,
        old_method_name=old_method_name,
        new_method_name=new_method_name,
        project_root=project_root
    )


def validate_method_name(method_name):
    """
    Validate that a method name follows Python naming conventions.
    
    Args:
        method_name (str): The method name to validate
    
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if valid, False otherwise
            - error_message (str): Error message if invalid, None if valid
    
    Example:
        >>> is_valid, error = validate_method_name('test_01_valid_name')
        >>> print(is_valid)
        True
        >>> is_valid, error = validate_method_name('123_invalid')
        >>> print(error)
        'Method name cannot start with a digit'
    """
    if not method_name:
        return False, "Method name cannot be empty"
    
    # Check if starts with digit
    if method_name[0].isdigit():
        return False, "Method name cannot start with a digit"
    
    # Check for valid Python identifier
    if not method_name.replace('_', '').replace('-', '').isalnum():
        return False, "Method name can only contain letters, digits, underscores, and hyphens"
    
    # Check for Python keywords
    python_keywords = [
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
        'try', 'while', 'with', 'yield'
    ]
    if method_name in python_keywords:
        return False, f"Method name cannot be a Python keyword: {method_name}"
    
    return True, None


if __name__ == "__main__":
    # Example usage and testing
    logging.basicConfig(level=logging.INFO)
    
    print("Method Rename Utility - Example Usage")
    print("=" * 60)
    
    # Example 1: Rename method
    print("\nExample 1: Rename method")
    result = rename_method_in_file(
        subfolder_name='TestComponent_01',
        file_name='TestClass_01',
        old_method_name='test_01_example',
        new_method_name='test_01_example_renamed'
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    # Example 2: Append to method name
    print("\nExample 2: Append to method name")
    result = append_to_method_name(
        subfolder_name='TestComponent_01',
        file_name='TestClass_01',
        old_method_name='test_01_example',
        append_text='updated'
    )
    print(f"Success: {result['success']}")
    print(f"New method name: {result['new_method_name']}")
    
    # Example 3: Validate method name
    print("\nExample 3: Validate method name")
    is_valid, error = validate_method_name('test_01_valid_name')
    print(f"Valid: {is_valid}, Error: {error}")
    
    is_valid, error = validate_method_name('123_invalid')
    print(f"Valid: {is_valid}, Error: {error}")
