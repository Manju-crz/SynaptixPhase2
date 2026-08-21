"""
File Rename Utility
Provides reusable functions to rename files within specified folders.
"""

import os
import logging

logger = logging.getLogger(__name__)


def rename_file_in_folder(folder_name, existing_file_name, new_file_name, project_root=None, search_recursive=True):
    """
    Rename a file within a specified folder.
    
    Args:
        folder_name (str): The folder name to search for (e.g., 'TestComponent_01')
        existing_file_name (str): The current file name (with or without extension)
        new_file_name (str): The new file name (with or without extension)
        project_root (str, optional): The project root directory. If None, auto-detects.
        search_recursive (bool, optional): Whether to search recursively for the folder. Defaults to True.
    
    Returns:
        dict: Result dictionary with keys:
            - success (bool): Whether the operation succeeded
            - message (str): Success or error message
            - old_file_name (str): The original file name
            - new_file_name (str): The new file name
            - old_file_path (str): The original path to the file
            - new_file_path (str): The new path to the file
    
    Example:
        >>> result = rename_file_in_folder(
        ...     'TestComponent_01',
        ...     'TestClass_01.py',
        ...     'TestClass_01_updated.py'
        ... )
        >>> print(result['success'])
        True
    """
    try:
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        logger.info(f"Searching for folder: {folder_name}")
        logger.info(f"  Existing file: {existing_file_name}")
        logger.info(f"  New file name: {new_file_name}")
        
        folder_path = None
        if search_recursive:
            folder_path = _find_folder_recursive(project_root, folder_name)
        else:
            potential_path = os.path.join(project_root, folder_name)
            if os.path.isdir(potential_path):
                folder_path = potential_path
        
        if folder_path is None:
            error_msg = f"Folder '{folder_name}' not found in project"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_file_name': existing_file_name,
                'new_file_name': new_file_name,
                'old_file_path': None,
                'new_file_path': None
            }
        
        old_file_path = os.path.join(folder_path, existing_file_name)
        
        if not os.path.exists(old_file_path):
            if not existing_file_name.endswith('.py'):
                existing_file_name_with_ext = f"{existing_file_name}.py"
                old_file_path_with_ext = os.path.join(folder_path, existing_file_name_with_ext)
                if os.path.exists(old_file_path_with_ext):
                    logger.info(f"File found with .py extension: {existing_file_name_with_ext}")
                    existing_file_name = existing_file_name_with_ext
                    old_file_path = old_file_path_with_ext
                else:
                    error_msg = f"File '{existing_file_name}' or '{existing_file_name_with_ext}' not found in folder '{folder_path}'"
                    logger.error(error_msg)
                    return {
                        'success': False,
                        'message': error_msg,
                        'old_file_name': existing_file_name,
                        'new_file_name': new_file_name,
                        'old_file_path': old_file_path,
                        'new_file_path': None
                    }
            else:
                error_msg = f"File '{existing_file_name}' not found in folder '{folder_path}'"
                logger.error(error_msg)
                return {
                    'success': False,
                    'message': error_msg,
                    'old_file_name': existing_file_name,
                    'new_file_name': new_file_name,
                    'old_file_path': old_file_path,
                    'new_file_path': None
                }
        
        if not os.path.isfile(old_file_path):
            error_msg = f"'{existing_file_name}' is not a file"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_file_name': existing_file_name,
                'new_file_name': new_file_name,
                'old_file_path': old_file_path,
                'new_file_path': None
            }
        
        if existing_file_name.endswith('.py') and not new_file_name.endswith('.py'):
            new_file_name = f"{new_file_name}.py"
            logger.info(f"Added .py extension to new file name: {new_file_name}")
        
        new_file_path = os.path.join(folder_path, new_file_name)
        
        if os.path.exists(new_file_path):
            error_msg = f"File '{new_file_name}' already exists in folder '{folder_path}'"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'old_file_name': existing_file_name,
                'new_file_name': new_file_name,
                'old_file_path': old_file_path,
                'new_file_path': new_file_path
            }
        
        os.rename(old_file_path, new_file_path)
        
        success_msg = f"Successfully renamed '{existing_file_name}' to '{new_file_name}' in folder '{folder_path}'"
        logger.info(success_msg)
        
        return {
            'success': True,
            'message': success_msg,
            'old_file_name': existing_file_name,
            'new_file_name': new_file_name,
            'old_file_path': old_file_path,
            'new_file_path': new_file_path
        }
    
    except Exception as e:
        error_msg = f"Error renaming file: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'success': False,
            'message': error_msg,
            'old_file_name': existing_file_name,
            'new_file_name': new_file_name,
            'old_file_path': old_file_path if 'old_file_path' in locals() else None,
            'new_file_path': new_file_path if 'new_file_path' in locals() else None
        }


def _find_folder_recursive(root_path, folder_name):
    """
    Recursively search for a folder by name.
    
    Args:
        root_path (str): The root path to start searching from
        folder_name (str): The folder name to search for
    
    Returns:
        str: The full path to the folder if found, None otherwise
    """
    for dirpath, dirnames, filenames in os.walk(root_path):
        if os.path.basename(dirpath) == folder_name:
            return dirpath
        
        for dirname in dirnames:
            if dirname == folder_name:
                return os.path.join(dirpath, dirname)
    
    return None


def rename_file_with_extension_handling(folder_name, existing_file_name, new_file_name, project_root=None, preserve_extension=True):
    """
    Rename a file with automatic extension handling.
    
    Args:
        folder_name (str): The folder name to search for
        existing_file_name (str): The current file name (with or without extension)
        new_file_name (str): The new file name (with or without extension)
        project_root (str, optional): The project root directory. If None, auto-detects.
        preserve_extension (bool, optional): If True and new_file_name has no extension, 
                                            use the extension from existing_file_name. Defaults to True.
    
    Returns:
        dict: Result dictionary (same format as rename_file_in_folder)
    
    Example:
        >>> result = rename_file_with_extension_handling(
        ...     'TestComponent_01',
        ...     'TestClass_01.py',
        ...     'TestClass_01_updated'
        ... )
        >>> print(result['new_file_name'])
        'TestClass_01_updated.py'
    """
    if preserve_extension:
        _, existing_ext = os.path.splitext(existing_file_name)
        _, new_ext = os.path.splitext(new_file_name)
        
        if existing_ext and not new_ext:
            new_file_name = new_file_name + existing_ext
            logger.info(f"Preserving extension: {existing_ext}")
    
    return rename_file_in_folder(
        folder_name=folder_name,
        existing_file_name=existing_file_name,
        new_file_name=new_file_name,
        project_root=project_root
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("File Rename Utility - Example Usage")
    print("=" * 60)
    
    print("\nExample 1: Rename file with full names")
    result = rename_file_in_folder(
        folder_name='TestComponent_01',
        existing_file_name='TestClass_01.py',
        new_file_name='TestClass_01_renamed.py'
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    print("\nExample 2: Rename file with extension handling")
    result = rename_file_with_extension_handling(
        folder_name='TestComponent_01',
        existing_file_name='TestClass_01.py',
        new_file_name='TestClass_01_updated'
    )
    print(f"Success: {result['success']}")
    print(f"New file name: {result['new_file_name']}")
