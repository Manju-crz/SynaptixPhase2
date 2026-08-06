"""
Test script for method_rename_util.py
This script tests the method renaming functionality explicitly.
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

# Add project root to path (parent directory of generator_altUtl)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from generator_altUtl.method_rename_util import (
    rename_method_in_file,
    append_to_method_name,
    validate_method_name
)

def print_separator(title=""):
    """Print a separator line"""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)

def test_validate_method_name():
    """Test the validate_method_name function"""
    print_separator("TEST 1: Validate Method Name")
    
    test_cases = [
        ("test_01_valid_name", True, None),
        ("test_create_pet_ai", True, None),
        ("123_invalid", False, "Method name cannot start with a digit"),
        ("", False, "Method name cannot be empty"),
        ("test-with-hyphens", True, None),
        ("class", False, "Method name cannot be a Python keyword: class"),
    ]
    
    for method_name, expected_valid, expected_error in test_cases:
        is_valid, error = validate_method_name(method_name)
        status = "[PASS]" if is_valid == expected_valid else "[FAIL]"
        print(f"\n{status} Testing: '{method_name}'")
        print(f"  Expected: valid={expected_valid}, error={expected_error}")
        print(f"  Got:      valid={is_valid}, error={error}")

def test_list_existing_methods(subfolder_name="TestComponent_01", file_name="TestClass_01"):
    """List all existing test methods in a test file"""
    print_separator("TEST 2: List Existing Methods")
    
    # Remove .py extension if provided
    if file_name.endswith('.py'):
        file_name = file_name[:-3]
    
    test_file = os.path.join(PROJECT_ROOT, "rest_test", subfolder_name, f"{file_name}.py")
    
    if not os.path.exists(test_file):
        print(f"[ERROR] Test file not found: {test_file}")
        return None
    
    print(f"[INFO] Reading file: {test_file}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all method definitions
    import re
    pattern = r'^\s+def\s+(test_\w+)\s*\('
    methods = re.findall(pattern, content, re.MULTILINE)
    
    print(f"\n[SUCCESS] Found {len(methods)} test methods:")
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")
    
    return methods

def test_append_to_method_name_interactive():
    """Interactive test for appending to method name"""
    print_separator("TEST 3: Append to Method Name (Interactive)")
    
    # Get user input for subfolder and file name first
    print("\n" + "-" * 80)
    print("Enter the details to test method renaming:")
    print("-" * 80)
    
    subfolder = input("Subfolder name (default: TestComponent_01): ").strip() or "TestComponent_01"
    file_name = input("File name (default: TestClass_01): ").strip() or "TestClass_01"
    
    # Remove .py extension if user added it
    if file_name.endswith('.py'):
        file_name = file_name[:-3]
    
    # Now list methods from the specified file
    print(f"\nListing methods from {subfolder}/{file_name}.py...")
    methods = test_list_existing_methods(subfolder_name=subfolder, file_name=file_name)
    if not methods:
        print("\n[ERROR] No methods found. Please check the file path and try again.")
        return
    
    print(f"\nAvailable methods in {file_name}.py:")
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")
    
    old_method = input("\nEnter the method name to rename (copy from above): ").strip()
    if not old_method:
        print("[ERROR] Method name cannot be empty")
        return
    
    if old_method not in methods:
        print(f"[WARNING]  Warning: Method '{old_method}' not found in the list above")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            return
    
    append_text = input("Enter text to append (e.g., 'updated', 'v2', 'modified'): ").strip()
    if not append_text:
        print("[ERROR] Append text cannot be empty")
        return
    
    # Show what will happen
    new_method_name = f"{old_method}_{append_text}"
    print("\n" + "-" * 80)
    print("[INFO] RENAME OPERATION SUMMARY:")
    print("-" * 80)
    print(f"  Subfolder:        {subfolder}")
    print(f"  File:             {file_name}.py")
    print(f"  Old method name:  {old_method}")
    print(f"  Append text:      {append_text}")
    print(f"  New method name:  {new_method_name}")
    print("-" * 80)
    
    confirm = input("\nProceed with renaming? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[ERROR] Operation cancelled")
        return
    
    # Perform the rename
    print("\n[RUNNING] Performing rename operation...")
    result = append_to_method_name(
        subfolder_name=subfolder,
        file_name=file_name,
        old_method_name=old_method,
        append_text=append_text,
        delimiter='_',
        project_root=PROJECT_ROOT
    )
    
    # Display result
    print("\n" + "=" * 80)
    if result['success']:
        print("[SUCCESS] SUCCESS!")
        print("=" * 80)
        print(f"  Message:          {result['message']}")
        print(f"  Old method name:  {result['old_method_name']}")
        print(f"  New method name:  {result['new_method_name']}")
        print(f"  File path:        {result['file_path']}")
        print("\n[TIP] You can verify the change by opening the test file.")
    else:
        print("[ERROR] FAILED!")
        print("=" * 80)
        print(f"  Error:            {result['message']}")
        print(f"  File path:        {result['file_path']}")
    print("=" * 80)

def test_append_to_method_name_automated():
    """Automated test with predefined values"""
    print_separator("TEST 4: Append to Method Name (Automated)")
    
    # Test with the most recent method
    methods = test_list_existing_methods()
    if not methods:
        print("\n[ERROR] No methods found. Skipping automated test.")
        return
    
    # Use the last method in the list
    old_method = methods[-1]
    
    test_params = {
        'subfolder_name': 'TestComponent_01',
        'file_name': 'TestClass_01',
        'old_method_name': old_method,
        'append_text': 'test_automated',
        'delimiter': '_',
        'project_root': PROJECT_ROOT
    }
    
    print("\n[INFO] Test Parameters:")
    for key, value in test_params.items():
        if key != 'project_root':
            print(f"  {key}: {value}")
    
    print("\n[WARNING]  WARNING: This will modify the actual test file!")
    confirm = input("Proceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[ERROR] Test cancelled")
        return
    
    print("\n[RUNNING] Running automated test...")
    result = append_to_method_name(**test_params)
    
    print("\n" + "=" * 80)
    if result['success']:
        print("[SUCCESS] AUTOMATED TEST PASSED!")
        print("=" * 80)
        print(f"  New method name: {result['new_method_name']}")
        print(f"  File: {result['file_path']}")
    else:
        print("[ERROR] AUTOMATED TEST FAILED!")
        print("=" * 80)
        print(f"  Error: {result['message']}")
    print("=" * 80)

def main():
    """Main test runner"""
    print("\n" + "=" * 80)
    print("  METHOD RENAME UTILITY - TEST SUITE")
    print("=" * 80)
    print("\nThis script tests the method_rename_util.py functionality.")
    print("Choose a test to run:")
    print("\n  1. Test validate_method_name()")
    print("  2. List existing test methods")
    print("  3. Interactive test - Append to method name")
    print("  4. Automated test - Append to method name")
    print("  5. Run all tests")
    print("  0. Exit")
    
    while True:
        print("\n" + "-" * 80)
        choice = input("Enter your choice (0-5): ").strip()
        
        if choice == '0':
            print("\n[BYE] Exiting test suite. Goodbye!")
            break
        elif choice == '1':
            test_validate_method_name()
        elif choice == '2':
            test_list_existing_methods()
        elif choice == '3':
            test_append_to_method_name_interactive()
        elif choice == '4':
            test_append_to_method_name_automated()
        elif choice == '5':
            test_validate_method_name()
            test_list_existing_methods()
            print("\n[WARNING]  Skipping interactive and automated tests in 'Run all' mode.")
            print("   Please run them individually if needed.")
        else:
            print("[ERROR] Invalid choice. Please enter 0-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[BYE] Test interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()

