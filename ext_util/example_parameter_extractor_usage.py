"""
Example usage of Parameter Extractor Utility
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ext_util.parameter_extractor_util import (
    ParameterExtractor,
    extract_and_print_parameters,
    extract_parameters_only
)

EXCEL_BASE_PATH = r"C:\BLKDeveloper\Synaptix\Rest_API_Data"


def example_1_simple_extraction():
    """Example 1: Extract and print parameters for a single Sl_No"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Parameter Extraction")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    sl_no = 2  # Create a new pet

    extract_and_print_parameters(excel_path, sl_no)


def example_2_multiple_extractions():
    """Example 2: Extract parameters for multiple Sl_Nos"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Multiple Parameter Extractions")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    sl_nos = [2, 3, 5, 8]  # Different API operations

    extractor = ParameterExtractor(excel_path)

    for sl_no in sl_nos:
        extractor.print_parameters(sl_no)
        print("\n" + "-"*80 + "\n")


def example_3_extract_without_printing():
    """Example 3: Extract parameters without printing (for programmatic use)"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Extract Parameters Programmatically")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    sl_no = 2

    # Extract without printing
    data = extract_parameters_only(excel_path, sl_no)

    if data['success']:
        print(f"\n✅ Successfully extracted parameters for SL_No {sl_no}")
        print(f"Method: {data['operation_method']}")
        print(f"Path: {data['operation_path']}")
        print(f"Summary: {data['operation_summary']}")

        # Use the data programmatically
        if data['header_parameters']:
            print(f"\nHeader Parameters Count: {len(data['header_parameters'])}")

        if data['query_parameters']:
            print(f"Query Parameters Count: {len(data['query_parameters'])}")

        if data['request_body_json']:
            print(f"Request Body Available: Yes")
            print(f"Request Body Keys: {list(data['request_body_json'].keys())}")
    else:
        print(f"\n❌ failed: {data['error']}")


def example_4_extract_from_generated_code():
    """Example 4: Extract parameters for SL_Nos used in code generation"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Extract Parameters from Generated Code SL_Nos")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")

    # These are the same SL_Nos that were used in code generation
    generated_sl_nos = [2, 3, 5]  # From test_pet_operations.py

    print(f"\nExtracting parameters for SL_Nos used in generated test code: {generated_sl_nos}\n")

    extractor = ParameterExtractor(excel_path)

    for i, sl_no in enumerate(generated_sl_nos, 1):
        print(f"\n{'-'*80}")
        print(f"Test {i} - SL_No: {sl_no}")
        print(f"{'-'*80}")
        extractor.print_parameters(sl_no)


def example_5_compare_parameters():
    """Example 5: Compare parameters between different operations"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Compare Parameters Between Operations")
    print("="*80)

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")

    # Compare POST vs PUT operations
    post_sl_no = 2  # POST /pet
    put_sl_no = 3   # PUT /pet

    extractor = ParameterExtractor(excel_path)

    post_data = extractor.extract_parameters(post_sl_no)
    put_data = extractor.extract_parameters(put_sl_no)

    print(f"\n🔵 Comparison:")
    print(f"\nPOST Operation (SL_No {post_sl_no}):")
    print(f"  Path: {post_data['operation_path']}")
    print(f"  Summary: {post_data['operation_summary']}")
    print(f"  Has Request Body: {'Yes' if post_data['request_body_json'] else 'No'}")

    print(f"\nPUT Operation (SL_No {put_sl_no}):")
    print(f"  Path: {put_data['operation_path']}")
    print(f"  Summary: {put_data['operation_summary']}")
    print(f"  Has Request Body: {'Yes' if put_data['request_body_json'] else 'No'}")


if __name__ == "__main__":
    print("\n" + "🚀 PARAMETER EXTRACTOR UTILITY EXAMPLES ".center(80, "="))

    # Run examples
    example_1_simple_extraction()
    example_2_multiple_extractions()
    example_3_extract_without_printing()
    example_4_extract_from_generated_code()
    example_5_compare_parameters()

    print("\n" + "=" * 80)
    print("✅ All examples completed!")
    print("=" + " \n")
