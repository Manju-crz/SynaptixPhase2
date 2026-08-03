"""
Example usage of Code Generator Utility
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator_util.code_generator_util import CodeGenerator, generate_tests_from_queries

EXCEL_BASE_PATH = r"C:\BLKDeveloper\Synaptix\Rest_API_Data"


def example_1_simple_generation():
    """Example 1: Generate test file from simple queries"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Test Generation")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    base_url = "https://petstore.swagger.io/v2"

    # Queries and their corresponding Sl_Nos from Excel
    queries = [
        "Create a new pet in the pet store",
        "Update an existing pet",
        "Find pet by ID"
    ]

    sl_nos = [2, 3, 5]  # Corresponding Sl_Nos from Excel

    folder_name = "generated_tests"
    filename = "test_pet_operations"

    result = generate_tests_from_queries(
        excel_path=excel_path,
        base_url=base_url,
        sl_nos=sl_nos,
        queries=queries,
        folder_name=folder_name,
        filename=filename
    )

    if result['success']:
        print(f"\n✅ SUCCESS!")
        print(f"   File: {result['file_path']}")
        print(f"   Tests Generated: {result['tests_generated']}")
        print(f"\n📄 Generated Tests:")
        for test in result['tests']:
            print(f"   - {test['query']} ({test['method']} {test['endpoint']})")
    else:
        print(f"\n❌ FAILED: {result['message']}")


def example_2_multiple_apis():
    """Example 2: Generate tests for multiple API operations"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Multiple API Operations")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    base_url = "https://petstore.swagger.io/v2"

    queries = [
        "Add a new pet to the store",
        "Update pet information",
        "Find pets by status",
        "Delete a pet",
        "Upload pet image"
    ]

    sl_nos = [2, 3, 6, 8, 10]

    folder_name = "pet_crud_tests"
    filename = "test_complete_pet_workflow"

    result = generate_tests_from_queries(
        excel_path=excel_path,
        base_url=base_url,
        sl_nos=sl_nos,
        queries=queries,
        folder_name=folder_name,
        filename=filename
    )

    if result['success']:
        print(f"\n✅ Test file created: {result['file_path']}")
        print(f"\nTo run the tests:")
        print(f"   pytest {result['file_path']} -v")
        print(f"\nWith Allure:")
        print(f"   pytest {result['file_path']} --alluredir=allure-results")
    else:
        print(f"\n❌ Error: {result['message']}")


def example_3_using_class():
    """Example 3: Using CodeGenerator class directly"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Using CodeGenerator Class")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    base_url = "https://petstore.swagger.io/v2"

    generator = CodeGenerator(
        excel_path=excel_path,
        base_url=base_url
    )

    queries = [
        "Create order for pet",
        "Get order by ID",
        "Delete order"
    ]

    sl_nos = [15, 16, 18]

    result = generator.generate_test_file(
        sl_nos=sl_nos,
        queries=queries,
        folder_name="store_tests",
        filename="test_order_management"
    )

    if result['success']:
        print(f"\n✅ Generated {result['tests_generated']} tests")
        print(f"   Location: {result['folder_path']}")
    else:
        print(f"\n❌ Failed: {result['error']}")


if __name__ == "__main__":
    print("\n" + "🚀 CODE GENERATOR UTILITY EXAMPLES ".center(80, "="))

    # Run examples
    example_1_simple_generation()
    example_2_multiple_apis()
    example_3_using_class()

    print("\n" + "="*80)
    print("✅ All examples completed!")
    print("="*80 + "\n")