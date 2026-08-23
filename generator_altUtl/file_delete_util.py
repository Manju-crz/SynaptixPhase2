"""
File Delete Utility
Provides reusable functions to delete test files or entire components from the rest_test folder.
"""

import os
import shutil
import logging

logger = logging.getLogger(__name__)


def delete_test_file(subfolder_name, file_name, project_root=None):
    """
    Delete a specific test file from a component folder in rest_test.

    Args:
        subfolder_name (str): The component/folder name (e.g., 'TestComponent_01')
        file_name (str): The file name to delete (e.g., 'TestClass_01.py')
        project_root (str, optional): The project root directory. If None, auto-detects.

    Returns:
        dict: Result dictionary with keys:
            - success (bool): Whether the operation succeeded
            - message (str): Success or error message
            - file_path (str): The path to the deleted file

    Example:
        >>> result = delete_test_file(
        ...     'TestComponent_01',
        ...     'TestClass_01.py'
        ... )
        >>> print(result['success'])
        True
    """
    try:
        # Auto-detect project root if not provided
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Validate inputs
        if not file_name:
            error_msg = "File name cannot be empty"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'file_path': ''
            }

        # Ensure .py extension
        if not file_name.endswith('.py'):
            file_name = f"{file_name}.py"

        # Construct the test file path
        test_file_path = os.path.join(project_root, "rest_test", subfolder_name, file_name)

        logger.info(f"Attempting to delete test file: {test_file_path}")

        # Check if file exists
        if not os.path.exists(test_file_path):
            error_msg = f"Test file not found: {test_file_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'file_path': test_file_path
            }

        # Check if it is actually a file
        if not os.path.isfile(test_file_path):
            error_msg = f"Path is not a file: {test_file_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'file_path': test_file_path
            }

        # Delete the file
        os.remove(test_file_path)

        success_msg = f"Successfully deleted file: {file_name}"
        logger.info(success_msg)

        return {
            'success': True,
            'message': success_msg,
            'file_path': test_file_path
        }

    except Exception as e:
        error_msg = f"Error deleting test file: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'success': False,
            'message': error_msg,
            'file_path': test_file_path if 'test_file_path' in locals() else 'unknown'
        }


def delete_component(subfolder_name, project_root=None):
    """
    Delete an entire component folder from rest_test, including all files inside it.

    Args:
        subfolder_name (str): The component/folder name (e.g., 'TestComponent_01')
        project_root (str, optional): The project root directory. If None, auto-detects.

    Returns:
        dict: Result dictionary with keys:
            - success (bool): Whether the operation succeeded
            - message (str): Success or error message
            - folder_path (str): The path to the deleted component folder

    Example:
        >>> result = delete_component('TestComponent_01')
        >>> print(result['success'])
        True
    """
    try:
        # Auto-detect project root if not provided
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Construct the component folder path
        component_folder_path = os.path.join(project_root, "rest_test", subfolder_name)

        logger.info(f"Attempting to delete component folder: {component_folder_path}")

        # Check if folder exists
        if not os.path.exists(component_folder_path):
            error_msg = f"Component folder not found: {component_folder_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'folder_path': component_folder_path
            }

        # Check if it is actually a directory
        if not os.path.isdir(component_folder_path):
            error_msg = f"Path is not a directory: {component_folder_path}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'folder_path': component_folder_path
            }

        # Delete the entire folder
        shutil.rmtree(component_folder_path)

        success_msg = f"Successfully deleted component folder: {subfolder_name}"
        logger.info(success_msg)

        return {
            'success': True,
            'message': success_msg,
            'folder_path': component_folder_path
        }

    except Exception as e:
        error_msg = f"Error deleting component folder: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'success': False,
            'message': error_msg,
            'folder_path': component_folder_path if 'component_folder_path' in locals() else 'unknown'
        }


if __name__ == "__main__":
    # Example usage and testing
    logging.basicConfig(level=logging.INFO)

    print("File Delete Utility - Example Usage")
    print("=" * 60)

    # Example 1: Delete a test file
    print("\nExample 1: Delete a test file")
    result = delete_test_file(
        subfolder_name='TestComponent_01',
        file_name='TestClass_01.py'
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"File path: {result['file_path']}")

    # Example 2: Delete an entire component
    print("\nExample 2: Delete a component folder")
    result = delete_component(
        subfolder_name='TestComponent_01'
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Folder path: {result['folder_path']}")
