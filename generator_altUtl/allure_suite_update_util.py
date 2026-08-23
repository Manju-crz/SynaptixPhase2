"""
Allure Suite Update Utility
Provides reusable functions to update the @allure.suite(...) annotation
in generated test files, keeping it in sync with the test class name.
"""

import re
import logging

logger = logging.getLogger(__name__)


def update_allure_suite(content, suite_name):
    """
    Update @allure.suite(...) annotation in the given content.

    Args:
        content (str): File content.
        suite_name (str): New suite name (usually the class name).

    Returns:
        tuple: (updated_content, count)
    """
    # Pattern: @allure.suite('...') or @allure.suite("...")
    pattern = re.compile(r'(@allure\.suite\()([\'"])(.*?)\2(\))', re.MULTILINE)
    new_content, count = pattern.subn(
        rf'\g<1>\g<2>{suite_name}\g<2>\g<4>',
        content,
        count=1
    )
    return new_content, count


def update_allure_suite_in_file(file_path, suite_name):
    """
    Update @allure.suite(...) in a file on disk.

    Args:
        file_path (str): Path to the Python test file.
        suite_name (str): New suite name.

    Returns:
        dict: Result with success, message, and count.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, count = update_allure_suite(content, suite_name)

        if count == 0:
            return {
                'success': True,
                'message': 'No @allure.suite annotation found to update',
                'count': 0
            }

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return {
            'success': True,
            'message': f'Updated @allure.suite to "{suite_name}"',
            'count': count
        }

    except Exception as e:
        logger.error(f"Error updating allure suite in {file_path}: {e}", exc_info=True)
        return {
            'success': False,
            'message': f'Error updating allure suite: {str(e)}',
            'count': 0
        }
