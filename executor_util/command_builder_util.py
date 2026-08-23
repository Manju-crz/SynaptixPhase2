"""
Command Builder Utility - Build pytest command strings for test execution
"""

import os
import ast
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class CommandBuilder:
    """
    Utility class to build pytest command strings for test execution.
    """

    def __init__(self, project_root: str = None):
        """
        Initialize CommandBuilder.

        Args:
            project_root: Root directory of the project (default: current directory)
        """
        self.project_root = project_root or os.getcwd()

    def build_pytest_command(
        self,
        folder_name: str,
        file_name: str,
        include_allure: bool = True,
        verbose: bool = True,
        show_output: bool = True,
        method_name: str = None,
        class_only: bool = False
    ) -> Optional[str]:
        """
        Build pytest command string for executing AI-generated test method.

        Args:
            folder_name: Test folder name (e.g., "test8")
            file_name: Test file name without .py extension (e.g., "test8")
            include_allure: Whether to include --alluredir flag (default: True)
            verbose: Whether to include -v flag (default: True)
            show_output: Whether to include -s flag (default: True)
            method_name: Specific test method name to execute. If provided, this
                        method is targeted directly. If None, falls back to finding
                        the first AI test method (ending with _ai) in the file.
            class_only: If True, target the class (all methods) instead of one method.

        Returns:
            Formatted pytest command string or None if error

        Example:
            >>> builder = CommandBuilder()
            >>> cmd = builder.build_pytest_command("test8", "test8", method_name="test_02_update_pet_ai")
            >>> print(cmd)
            pytest .\\rest_test\\test8\\test8.py::TestGeneratedAPIs::test_02_update_pet_ai -v -s --alluredir=allure-results
        """
        try:
            # Build file path
            file_path = os.path.join(self.project_root, "rest_test", folder_name, f"{file_name}.py")

            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"Test file not found: {file_path}")
                return None

            # Read class name from file
            class_name = self._get_test_class_name(file_path)
            if not class_name:
                logger.error(f"No test class found in {file_path}")
                return None

            # Build relative path for pytest
            relative_path = f".\\rest_test\\{folder_name}\\{file_name}.py"

            if class_only:
                # Target the whole class (all methods)
                test_selector = f"{relative_path}::{class_name}"
            else:
                # Determine which method to execute
                if method_name:
                    # Use the explicitly provided method name
                    target_method = method_name
                    logger.info(f"Using specified test method: {target_method}")
                else:
                    # Fall back to finding the first AI test method
                    target_method = self._find_ai_test_method(file_path, class_name)
                    if not target_method:
                        logger.error(f"No AI test method (ending with _ai) found in {file_path}")
                        return None

                # Build command - concatenate path and test selector without space
                test_selector = f"{relative_path}::{class_name}::{target_method}"

            command_parts = [
                "pytest",
                test_selector
            ]

            # Add flags
            if verbose:
                command_parts.append("-v")
            if show_output:
                command_parts.append("-s")
            if include_allure:
                command_parts.append("--alluredir=allure-results")

            command = " ".join(command_parts)
            logger.info(f"Built command: {command}")

            return command

        except Exception as e:
            logger.error(f"Error building pytest command: {str(e)}")
            return None

    def _get_test_class_name(self, file_path: str) -> Optional[str]:
        """
        Extract test class name from Python file using AST.

        Args:
            file_path: Path to the test file

        Returns:
            Test class name or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            tree = ast.parse(file_content)

            # Find class that starts with 'Test'
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.name.startswith('Test'):
                        logger.info(f"Found test class: {node.name}")
                        return node.name

            return None

        except Exception as e:
            logger.error(f"Error reading class name from {file_path}: {str(e)}")
            return None

    def _find_ai_test_method(self, file_path: str, class_name: str) -> Optional[str]:
        """
        Find test method ending with '_ai' in the specified class.

        Args:
            file_path: Path to the test file
            class_name: Name of the test class

        Returns:
            AI test method name or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            tree = ast.parse(file_content)

            # Find the target class
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    # Look for methods in this class
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if item.name.startswith('test_') and item.name.endswith('_ai'):
                                logger.info(f"Found AI test method: {item.name}")
                                return item.name

            return None

        except Exception as e:
            logger.error(f"Error finding AI test method: {str(e)}")
            return None

    def get_all_ai_test_methods(self, file_path: str) -> List[str]:
        """
        Get all test methods ending with '_ai' from a file.

        Args:
            file_path: Path to the test file

        Returns:
            List of AI test method names
        """
        ai_methods = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            tree = ast.parse(file_content)

            # Find all test classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name.startswith('Test'):
                    # Look for methods in this class
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if item.name.startswith('test_') and item.name.endswith('_ai'):
                                ai_methods.append(item.name)

            logger.info(f"Found {len(ai_methods)} AI test methods")
            return ai_methods

        except Exception as e:
            logger.error(f"Error getting AI test methods: {str(e)}")
            return []


def build_pytest_command(
    folder_name: str,
    file_name: str,
    include_allure: bool = True,
    project_root: str = None,
    method_name: str = None,
    class_only: bool = False
) -> Optional[str]:
    """
    Convenience function to build pytest command string.

    Args:
        folder_name: Test folder name (e.g., "test8")
        file_name: Test file name without .py extension (e.g., "test8")
        include_allure: Whether to include --alluredir flag
        project_root: Project root directory
        method_name: Specific test method name to execute (optional). If None,
                    falls back to the first AI test method in the file.
        class_only: If True, target the whole class (all methods).

    Returns:
        Formatted pytest command string or None

    Example:
        >>> cmd = build_pytest_command("test8", "test8", method_name="test_02_update_pet_ai")
        >>> print(cmd)
        pytest .\\rest_test\\test8\\test8.py::TestGeneratedAPIs::test_02_update_pet_ai -v -s --alluredir=allure-results
    """
    builder = CommandBuilder(project_root)
    return builder.build_pytest_command(folder_name, file_name, include_allure, method_name=method_name, class_only=class_only)