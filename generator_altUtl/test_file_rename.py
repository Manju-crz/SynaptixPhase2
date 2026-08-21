"""
Test File Rename Utility
Comprehensive tests for file_rename_util.py
"""

import os
import sys
import logging
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator_altUtl.file_rename_util import (
    rename_file_in_folder,
    rename_file_with_extension_handling,
    _find_folder_recursive
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestFileRenameUtility:
    """Test suite for file rename utility functions"""
    
    def __init__(self):
        self.test_root = None
        self.test_results = []
    
    def setup_test_environment(self):
        """Create a temporary test directory structure"""
        logger.info("Setting up test environment...")
        
        self.test_root = tempfile.mkdtemp(prefix="test_file_rename_")
        logger.info(f"Created test root: {self.test_root}")
        
        test_folder_1 = os.path.join(self.test_root, "TestComponent_01")
        test_folder_2 = os.path.join(self.test_root, "rest_test", "TestComponent_02")
        test_folder_3 = os.path.join(self.test_root, "nested", "deep", "TestFolder")
        
        os.makedirs(test_folder_1, exist_ok=True)
        os.makedirs(test_folder_2, exist_ok=True)
        os.makedirs(test_folder_3, exist_ok=True)
        
        test_file_1 = os.path.join(test_folder_1, "test_file.py")
        test_file_2 = os.path.join(test_folder_1, "another_file.txt")
        test_file_3 = os.path.join(test_folder_2, "deep_test.py")
        test_file_4 = os.path.join(test_folder_3, "nested_file.json")
        
        with open(test_file_1, 'w') as f:
            f.write("# Test Python file\nprint('Hello World')\n")
        
        with open(test_file_2, 'w') as f:
            f.write("This is a text file\n")
        
        with open(test_file_3, 'w') as f:
            f.write("# Deep nested test file\n")
        
        with open(test_file_4, 'w') as f:
            f.write('{"test": "data"}\n')
        
        logger.info("Test environment setup complete")
        return True
    
    def teardown_test_environment(self):
        """Clean up temporary test directory"""
        if self.test_root and os.path.exists(self.test_root):
            logger.info(f"Cleaning up test environment: {self.test_root}")
            shutil.rmtree(self.test_root)
            logger.info("Test environment cleaned up")
    
    def run_test(self, test_name, test_func):
        """Run a single test and record results"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*60}")
        
        try:
            result = test_func()
            self.test_results.append({
                'test_name': test_name,
                'status': 'PASSED' if result else 'FAILED',
                'result': result
            })
            logger.info(f"✓ {test_name}: {'PASSED' if result else 'FAILED'}")
            return result
        except Exception as e:
            logger.error(f"✗ {test_name}: FAILED with exception: {str(e)}", exc_info=True)
            self.test_results.append({
                'test_name': test_name,
                'status': 'ERROR',
                'result': str(e)
            })
            return False
    
    def test_basic_file_rename(self):
        """Test basic file rename functionality"""
        result = rename_file_in_folder(
            folder_name='TestComponent_01',
            existing_file_name='test_file.py',
            new_file_name='renamed_test_file.py',
            project_root=self.test_root
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == True, "Rename should succeed"
        assert result['old_file_name'] == 'test_file.py', "Old file name mismatch"
        assert result['new_file_name'] == 'renamed_test_file.py', "New file name mismatch"
        assert os.path.exists(result['new_file_path']), "New file should exist"
        assert not os.path.exists(result['old_file_path']), "Old file should not exist"
        
        return True
    
    def test_rename_different_extension(self):
        """Test renaming file with different extension"""
        result = rename_file_in_folder(
            folder_name='TestComponent_01',
            existing_file_name='another_file.txt',
            new_file_name='another_file.md',
            project_root=self.test_root
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == True, "Rename should succeed"
        assert result['new_file_name'] == 'another_file.md', "Extension should change"
        assert os.path.exists(result['new_file_path']), "New file should exist"
        
        return True
    
    def test_rename_nested_folder(self):
        """Test renaming file in deeply nested folder"""
        result = rename_file_in_folder(
            folder_name='TestComponent_02',
            existing_file_name='deep_test.py',
            new_file_name='deep_test_renamed.py',
            project_root=self.test_root
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == True, "Rename should succeed for nested folder"
        assert 'TestComponent_02' in result['new_file_path'], "Path should contain folder name"
        
        return True
    
    def test_rename_with_extension_handling(self):
        """Test automatic extension preservation"""
        result = rename_file_with_extension_handling(
            folder_name='TestFolder',
            existing_file_name='nested_file.json',
            new_file_name='nested_file_updated',
            project_root=self.test_root,
            preserve_extension=True
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == True, "Rename should succeed"
        assert result['new_file_name'] == 'nested_file_updated.json', "Extension should be preserved"
        assert os.path.exists(result['new_file_path']), "New file should exist"
        
        return True
    
    def test_folder_not_found(self):
        """Test error handling when folder doesn't exist"""
        result = rename_file_in_folder(
            folder_name='NonExistentFolder',
            existing_file_name='test.py',
            new_file_name='renamed.py',
            project_root=self.test_root
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == False, "Should fail when folder not found"
        assert 'not found' in result['message'].lower(), "Error message should mention not found"
        
        return True
    
    def test_file_not_found(self):
        """Test error handling when file doesn't exist"""
        result = rename_file_in_folder(
            folder_name='TestComponent_01',
            existing_file_name='non_existent_file.py',
            new_file_name='renamed.py',
            project_root=self.test_root
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == False, "Should fail when file not found"
        assert 'not found' in result['message'].lower(), "Error message should mention not found"
        
        return True
    
    def test_target_file_already_exists(self):
        """Test error handling when target file already exists"""
        folder_path = os.path.join(self.test_root, "TestComponent_01")
        existing_file = os.path.join(folder_path, "file_to_rename.py")
        target_file = os.path.join(folder_path, "existing_target.py")
        
        with open(existing_file, 'w') as f:
            f.write("# File to rename\n")
        
        with open(target_file, 'w') as f:
            f.write("# Already exists\n")
        
        result = rename_file_in_folder(
            folder_name='TestComponent_01',
            existing_file_name='file_to_rename.py',
            new_file_name='existing_target.py',
            project_root=self.test_root
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == False, "Should fail when target already exists"
        assert 'already exists' in result['message'].lower(), "Error message should mention already exists"
        
        return True
    
    def test_find_folder_recursive(self):
        """Test recursive folder finding"""
        found_path = _find_folder_recursive(self.test_root, 'TestFolder')
        
        logger.info(f"Found path: {found_path}")
        
        assert found_path is not None, "Should find nested folder"
        assert 'TestFolder' in found_path, "Path should contain folder name"
        assert os.path.exists(found_path), "Found path should exist"
        
        return True
    
    def test_non_recursive_search(self):
        """Test non-recursive folder search"""
        result = rename_file_in_folder(
            folder_name='TestComponent_02',
            existing_file_name='deep_test_renamed.py',
            new_file_name='final_name.py',
            project_root=self.test_root,
            search_recursive=False
        )
        
        logger.info(f"Result: {result}")
        
        assert result['success'] == False, "Should fail with non-recursive search for nested folder"
        
        return True
    
    def print_summary(self):
        """Print test summary"""
        logger.info(f"\n{'='*60}")
        logger.info("TEST SUMMARY")
        logger.info(f"{'='*60}")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['status'] == 'PASSED')
        failed_tests = sum(1 for r in self.test_results if r['status'] == 'FAILED')
        error_tests = sum(1 for r in self.test_results if r['status'] == 'ERROR')
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Errors: {error_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.2f}%")
        
        logger.info(f"\nDetailed Results:")
        for result in self.test_results:
            status_symbol = '✓' if result['status'] == 'PASSED' else '✗'
            logger.info(f"  {status_symbol} {result['test_name']}: {result['status']}")
        
        logger.info(f"{'='*60}\n")


def run_all_tests():
    """Run all tests"""
    test_suite = TestFileRenameUtility()
    
    try:
        test_suite.setup_test_environment()
        
        test_suite.run_test("Test 1: Basic File Rename", test_suite.test_basic_file_rename)
        test_suite.run_test("Test 2: Rename with Different Extension", test_suite.test_rename_different_extension)
        test_suite.run_test("Test 3: Rename in Nested Folder", test_suite.test_rename_nested_folder)
        test_suite.run_test("Test 4: Extension Handling", test_suite.test_rename_with_extension_handling)
        test_suite.run_test("Test 5: Folder Not Found Error", test_suite.test_folder_not_found)
        test_suite.run_test("Test 6: File Not Found Error", test_suite.test_file_not_found)
        test_suite.run_test("Test 7: Target File Already Exists", test_suite.test_target_file_already_exists)
        test_suite.run_test("Test 8: Recursive Folder Finding", test_suite.test_find_folder_recursive)
        test_suite.run_test("Test 9: Non-Recursive Search", test_suite.test_non_recursive_search)
        
        test_suite.print_summary()
        
    finally:
        test_suite.teardown_test_environment()


def test_with_real_project():
    """Test with real project structure (use carefully!)"""
    logger.info("\n" + "="*60)
    logger.info("REAL PROJECT TEST (Read-Only)")
    logger.info("="*60)
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    logger.info("\nTest: Finding existing folders in project")
    
    test_folders = ['rest_test', 'generator_util', 'executor_util']
    
    for folder in test_folders:
        found_path = _find_folder_recursive(project_root, folder)
        if found_path:
            logger.info(f"✓ Found '{folder}' at: {found_path}")
        else:
            logger.info(f"✗ Could not find '{folder}'")
    
    logger.info("\nNote: Actual file rename operations are skipped in real project test")
    logger.info("="*60 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FILE RENAME UTILITY - TEST SUITE")
    print("="*60 + "\n")
    
    print("Choose test mode:")
    print("1. Run all tests (creates temporary test environment)")
    print("2. Test folder finding with real project (read-only)")
    print("3. Run both")
    
    choice = input("\nEnter choice (1/2/3) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        run_all_tests()
    elif choice == "2":
        test_with_real_project()
    elif choice == "3":
        run_all_tests()
        test_with_real_project()
    else:
        print("Invalid choice. Running all tests...")
        run_all_tests()
    
    print("\n" + "="*60)
    print("TEST EXECUTION COMPLETE")
    print("="*60 + "\n")
