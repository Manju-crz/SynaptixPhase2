"""
File Utilities - Reusable file and folder operations
"""

import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def create_folder_if_not_exists(folder_path: str) -> bool:
    """
    Create a folder if it does not already exist.

    Args:
        folder_path: Path to the folder to create

    Returns:
        bool: True if folder was created, False if it already existed
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"✅ Folder created: {folder_path}")
        return True
    else:
        logger.info(f"ℹ️ Folder already exists: {folder_path}")
        return False


def create_file(folder_path: str, filename: str, extension: str, content: str = "") -> str:
    """
    Create a new file with the given filename and extension.

    Args:
        folder_path: Path to the folder where file will be created
        filename: Name of the file (without extension)
        extension: File extension (e.g., 'txt', 'json', 'py')
        content: Optional content to write to the file

    Returns:
        str: Full path to the created file
    """
    # Ensure folder exists
    create_folder_if_not_exists(folder_path)

    # Remove leading dot from extension if provided
    extension = extension.lstrip('.')

    # Build full file path
    full_filename = f"{filename}.{extension}"
    file_path = os.path.join(folder_path, full_filename)

    # Create the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"✅ File created: {file_path}")
    return file_path
