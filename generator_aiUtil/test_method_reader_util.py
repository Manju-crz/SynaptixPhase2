"""
Test Method Reader Utility - Read and extract complete test method code from generated test files
Reads test methods with all their steps from Python test files
"""

import os
import ast
import logging
from typing import Dict, List, Optional, Any

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class TestMethodReader:
    """
    Reads and extracts complete test method code from generated test files.
    """

    def __init__(self, file_path: str):
        """
        Initialize Test Method Reader.

        Args:
            file_path: Path to the Python test file
        """
        self.file_path = file_path
        logger.info(f"📖 Initializing Test Method Reader")
        logger.info(f"  File: {file_path}")

    def _read_file_content(self) -> Optional[str]:
        """
        Read the complete file content.

        Returns:
            File content as string or None if error
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            logger.error(f"❌ Error reading file: {str(e)}")
            return None

    def _extract_method_code(self, content: str, method_name: str) -> Optional[str]:
        """
        Extract the complete code of a specific method.

        Args:
            content: File content
            method_name: Name of the method to extract

        Returns:
            Method code as string or None if not found
        """
        try:
            # Parse the file into AST
            tree = ast.parse(content)

            # Find the method
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == method_name:
                    # Get the line numbers
                    start_line = node.lineno - 1  # 0-indexed
                    end_line = node.end_lineno
                    # Extract the lines
                    lines = content.split('\n')
                    method_lines = lines[start_line:end_line]
                    return '\n'.join(method_lines)

            logger.warning(f"⚠️  Method '{method_name}' not found in file")
            return None

        except Exception as e:
            logger.error(f"❌ Error extracting method: {str(e)}")
            return None

    def get_all_test_methods(self) -> List[str]:
        """
        Get list of all test method names in the file.

        Returns:
            List of test method names
        """
        try:
            content = self._read_file_content()
            if not content:
                return []

            tree = ast.parse(content)
            test_methods = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name.startswith('test_'):
                        test_methods.append(node.name)

            return test_methods

        except Exception as e:
            logger.error(f"❌ Error getting test methods: {str(e)}")
            return []

    def read_test_method(self, method_name: str) -> Dict[str, Any]:
        """
        Read complete test method code.

        Args:
            method_name: Name of the test method

        Returns:
            Dictionary with method details and code
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"📖 READING TEST METHOD: {method_name}")
        logger.info(f"{'='*80}")

        content = self._read_file_content()
        if not content:
            return {
                'success': False,
                'error': 'Failed to read file',
                'method_name': method_name
            }

        method_code = self._extract_method_code(content, method_name)
        if not method_code:
            return {
                'success': False,
                'error': f"Method '{method_name}' not found",
                'method_name': method_name
            }

        # Count steps in the method
        step_count = method_code.count('with allure.step(')

        return {
            'success': True,
            'method_name': method_name,
            'file_path': self.file_path,
            'code': method_code,
            'line_count': len(method_code.split('\n')),
            'step_count': step_count
        }

    def print_test_method(self, method_name: str):
        """
        Read and print complete test method code.

        Args:
            method_name: Name of the test method
        """
        result = self.read_test_method(method_name)

        if not result['success']:
            logger.error(f"❌ {result['error']}")
            return

        logger.info(f"\n{'='*80}")
        logger.info(f"📋 TEST METHOD DETAILS")
        logger.info(f"{'='*80}")
        logger.info(f"Method Name: {result['method_name']}")
        logger.info(f"File Path: {result['file_path']}")
        logger.info(f"Line Count: {result['line_count']}")
        logger.info(f"Step Count: {result['step_count']}")

        logger.info(f"\n{'='*80}")
        logger.info(f"📄 METHOD CODE")
        logger.info(f"{'='*80}\n")

        print(result['code'])

        logger.info(f"\n{'='*80}\n")

    def print_all_test_methods(self):
        """
        Print all test methods in the file.
        """
        methods = self.get_all_test_methods()

        if not methods:
            logger.warning("⚠️  No test methods found in file")
            return

        logger.info(f"\n{'='*80}")
        logger.info(f"📚 ALL TEST METHODS IN FILE")
        logger.info(f"{'='*80}")
        logger.info(f"Total Methods: {len(methods)}\n")

        for i, method in enumerate(methods, 1):
            logger.info(f"{i}. {method}")

        logger.info(f"\n{'='*80}\n")
        logger.info("Reading all methods...")
        logger.info(f"{'='*80}\n")

        for method in methods:
            self.print_test_method(method)
            print("\n" + "-"*80 + "\n")


def read_and_print_test_method(file_path: str, method_name: str):
    """
    Convenience function to read and print a test method.

    Args:
        file_path: Path to the test file
        method_name: Name of the test method
    """
    reader = TestMethodReader(file_path)
    reader.print_test_method(method_name)


def get_test_method_code(file_path: str, method_name: str) -> Dict[str, Any]:
    """
    Convenience function to get test method code without printing.

    Args:
        file_path: Path to the test file
        method_name: Name of the test method

    Returns:
        Dictionary with method details and code
    """
    reader = TestMethodReader(file_path)
    return reader.read_test_method(method_name)


def list_all_test_methods(file_path: str) -> List[str]:
    """
    Convenience function to list all test methods in a file.

    Args:
        file_path: Path to the test file

    Returns:
        List of test method names
    """
    reader = TestMethodReader(file_path)
    return reader.get_all_test_methods()