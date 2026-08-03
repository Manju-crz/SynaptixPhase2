"""
Example usage of Test Method Reader Utility
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator_aiUtil.test_method_reader_util import (
    TestMethodReader,
    read_and_print_test_method,
    get_test_method_code,
    list_all_test_methods
)

REST_TEST_BASE = r"C:\BLKDeveloper\Synaptix\rest_test"


def example_1_read_single_method():
    """Example 1: Read and print a single test method"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Read Single Test Method")
    print("="*80)

    # Read from the twenty.py file you showed
    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")
    method_name = "test_01_create_a_new_pet"

    read_and_print_test_method(file_path, method_name)


def example_2_list_all_methods():
    """Example 2: List all test methods in a file"""
    print("\n" + "="*80)
    print("EXAMPLE 2: List All Test Methods")
    print("="*80)

    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")

    methods = list_all_test_methods(file_path)

    print(f"\nFound {len(methods)} test methods:")
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")


def example_3_read_without_printing():
    """Example 3: Read method code without printing (for programmatic use)"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Read Method Code Programmatically")
    print("="*80)

    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")
    method_name = "test_01_create_a_new_pet"

    result = get_test_method_code(file_path, method_name)

    if result['success']:
        print(f"\n✅ Successfully read method: {result['method_name']}")
        print(f"  Lines: {result['line_count']}")
        print(f"  Steps: {result['step_count']}")
        print(f"\n  First 5 lines of code:")
        lines = result['code'].split('\n')[:5]
        for line in lines:
            print(f"  {line}")
    else:
        print(f"\n❌ Failed: {result['error']}")


def example_4_read_all_methods_in_file():
    """Example 4: Read all test methods in a file"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Read All Test Methods in File")
    print("="*80)

    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")

    reader = TestMethodReader(file_path)
    reader.print_all_test_methods()


def example_5_read_from_generated_folder():
    """Example 5: Read methods from different generated test folders"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Read from Generated Test Folders")
    print("="*80)

    # Example folders created by code generator
    test_folders = [
        ("generated_tests", "test_pet_operations.py"),
        ("pet_crud_tests", "test_complete_pet_workflow.py"),
        ("store_tests", "test_order_management.py")
    ]

    for folder, filename in test_folders:
        file_path = os.path.join(REST_TEST_BASE, folder, filename)

        if os.path.exists(file_path):
            print(f"\n{'='*80}")
            print(f"Reading from: {folder}/{filename}")
            print(f"{'='*80}")

            methods = list_all_test_methods(file_path)
            print(f"\nFound {len(methods)} test methods:")
            for method in methods:
                print(f"  - {method}")
        else:
            print(f"\n⚠️  File not found: {folder}/{filename}")


def example_6_analyze_method_steps():
    """Example 6: Analyze steps in test methods"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Analyze Method Steps")
    print("="*80)

    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")

    reader = TestMethodReader(file_path)
    methods = reader.get_all_test_methods()

    print(f"\nAnalyzing {len(methods)} test methods:\n")

    for method in methods:
        result = reader.read_test_method(method)
        if result['success']:
            print(f"Method: {result['method_name']}")
            print(f"  Lines: {result['line_count']}")
            print(f"  Steps: {result['step_count']}")
            print()


if __name__ == "__main__":
    print("\n" + " TEST METHOD READER UTILITY EXAMPLES ".center(80, "="))

    # Run examples
    example_1_read_single_method()
    example_2_list_all_methods()
    example_3_read_without_printing()
    example_4_read_all_methods_in_file()
    example_5_read_from_generated_folder()
    example_6_analyze_method_steps()

    print("\n" + "="*80)
    print("✅ All examples completed!")
    print("="*80 + "\n")