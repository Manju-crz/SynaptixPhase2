"""
Example usage of AI Code Modifier Utility
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator_aiUtil.ai_code_modifier_util import AICodeModifier, modify_generated_code_with_ai
from generator_aiUtil.test_method_reader_util import TestMethodReader
from ext_util.parameter_extractor_util import ParameterExtractor

REST_TEST_BASE = r"C:\BLKDeveloper\Synaptix\rest_test"
EXCEL_BASE_PATH = r"C:\BLKDeveloper\Synaptix\Rest_API_Data"


def example_1_modify_with_openai():
    """Example 1: Modify generated code using OpenAI"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Modify Code with OpenAI")
    print("="*80)

    # File and method info
    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")
    method_name = "test_01_create_a_new_pet"

    # Read original code
    reader = TestMethodReader(file_path)
    result = reader.read_test_method(method_name)
    original_code = result['code']

    # Queries with instructions (using -> delimiter)
    queries = [
        "Create a new pet -> Retrieve the pet_id from the response",
        "Update pet information -> Use the pet_id from previous response",
        "Delete a pet -> Use the pet_id from previous response"
    ]

    # Extract Excel data for each step (Sl_Nos: 2, 3, 8)
    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    extractor = ParameterExtractor(excel_path)

    excel_data = []
    for sl_no in [2, 3, 8]:
        data = extractor.extract_parameters(sl_no)
        excel_data.append(data)

    # Modify code with AI
    modified_result = modify_generated_code_with_ai(
        file_path=file_path,
        method_name=method_name,
        original_code=original_code,
        excel_data=excel_data,
        queries=queries,
        ai_provider="openai"
    )

    if modified_result['success']:
        print(f"\n✅ Code modified successfully!")
        print(f"  New method: {modified_result['new_method_name']}")
        print(f"  File: {modified_result['file_path']}")
        print(f"  Instructions applied: {modified_result['instructions_applied']}")
    else:
        print(f"\n❌ Failed: {modified_result.get('error')}")


def example_2_modify_with_groq():
    """Example 2: Modify generated code using Groq (faster)"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Modify Code with Groq (Ultra-fast)")
    print("="*80)

    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")
    method_name = "test_01_create_a_new_pet"

    reader = TestMethodReader(file_path)
    result = reader.read_test_method(method_name)
    original_code = result['code']

    queries = [
        "Create a new pet -> Extract id and name from response -> Store for later use",
        "Update pet information -> Use the id from step 1 -> Change status to sold",
        "Delete a pet -> Use the id from step 1"
    ]

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    extractor = ParameterExtractor(excel_path)

    excel_data = [extractor.extract_parameters(sl_no) for sl_no in [2, 3, 8]]

    modified_result = modify_generated_code_with_ai(
        file_path=file_path,
        method_name=method_name,
        original_code=original_code,
        excel_data=excel_data,
        queries=queries,
        ai_provider="groq"  # Using Groq for faster response
    )

    if modified_result['success']:
        print(f"\n✅ Code modified with Groq!")
        print(f"  New method: {modified_result['new_method_name']}")


def example_3_modify_with_deepseek():
    """Example 3: Modify generated code using DeepSeek (code specialist)"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Modify Code with DeepSeek (Code Specialist)")
    print("="*80)

    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")
    method_name = "test_01_create_a_new_pet"

    reader = TestMethodReader(file_path)
    result = reader.read_test_method(method_name)
    original_code = result['code']

    queries = [
        "Create a new pet -> Get the pet_id from response",
        "Update pet information -> Use pet_id from previous step",
        "Delete a pet -> Use pet_id from step 1"
    ]

    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    extractor = ParameterExtractor(excel_path)

    excel_data = [extractor.extract_parameters(sl_no) for sl_no in [2, 3, 8]]

    modified_result = modify_generated_code_with_ai(
        file_path=file_path,
        method_name=method_name,
        original_code=original_code,
        excel_data=excel_data,
        queries=queries,
        ai_provider="deepseek"  # Using DeepSeek for code-focused modifications
    )

    if modified_result['success']:
        print(f"\n✅ Code modified with DeepSeek!")
        print(f"  New method: {modified_result['new_method_name']}")


def example_4_class_usage():
    """Example 4: Using the AICodeModifier class directly"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Direct Class Usage")
    print("="*80)

    # Initialize modifier
    modifier = AICodeModifier(ai_provider="openai")

    # Get original code
    file_path = os.path.join(REST_TEST_BASE, "twenty", "twenty.py")
    reader = TestMethodReader(file_path)
    result = reader.read_test_method("test_01_create_a_new_pet")
    original_code = result['code']

    # Get Excel data
    excel_path = os.path.join(EXCEL_BASE_PATH, "PetStore_Data.xlsx")
    extractor = ParameterExtractor(excel_path)
    excel_data = [extractor.extract_parameters(sl_no) for sl_no in [2, 3, 8]]

    # Queries
    queries = [
        "Create a new pet -> Extract pet_id",
        "Update pet information -> Use pet_id",
        "Delete a pet -> Use pet_id"
    ]

    # Modify code
    mod_result = modifier.modify_code_with_ai(original_code, excel_data, queries)

    if mod_result['success']:
        print(f"\n✅ Code modified!")
        print(f"  Lines: {len(mod_result['modified_code'].split(chr(10)))}")

        # Append to file
        append_result = modifier.append_modified_method_to_file(
            file_path,
            "test_01_create_a_new_pet",
            mod_result['modified_code']
        )

        if append_result['success']:
            print(f"  Appended as: {append_result['new_method_name']}")


if __name__ == "__main__":
    print("\n" + " AI CODE MODIFIER UTILITY EXAMPLES ".center(80, "="))

    # Run examples (choose one to avoid multiple AI calls)
    example_1_modify_with_openai()
    # example_2_modify_with_groq()
    # example_3_modify_with_deepseek()
    # example_4_class_usage()

    print("\n" + "="*80)
    print("✅ Examples completed!")
    print("="*80 + "\n")