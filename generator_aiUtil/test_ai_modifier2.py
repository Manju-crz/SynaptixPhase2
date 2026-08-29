"""
Quick test runner for ai_code_modifier_util2.py

Usage from project root:
    python generator_aiUtil\\test_ai_modifier2.py <path_to_test_file> <method_name> [ai_provider]

Or as a module:
    python -m generator_aiUtil.test_ai_modifier2 <path_to_test_file> <method_name> [ai_provider]

Example:
    python generator_aiUtil\\test_ai_modifier2.py rest_test\\Ag29\\TestFile_03.py test_01_authenticate_login_to_retrieve_temporary_access_token_ai openai

The script:
- Uses the default STANDARD_METHOD_ENHANCEMENT_PROMPT from prompts.py
- Creates a .bak backup of the original file
- Calls the AI enhancer for the specified method
- Prints the result
"""

import os
import sys
import shutil

# Allow running this script directly from inside generator_aiUtil
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from generator_aiUtil.ai_code_modifier_util2 import enhance_test_method_with_ai


def main():
    if len(sys.argv) < 3:
        print("Usage: python generator_aiUtil\\test_ai_modifier2.py <path_to_test_file> <method_name> [ai_provider]")
        print("Example: python generator_aiUtil\\test_ai_modifier2.py rest_test\\Ag29\\TestFile_03.py test_01_my_method openai")
        return

    file_path = sys.argv[1]
    method_name = sys.argv[2]
    ai_provider = sys.argv[3] if len(sys.argv) > 3 else "openai"

    print(f"Target file: {file_path}")
    print(f"Method name: {method_name}")
    print(f"AI provider: {ai_provider}")

    # Create a backup before the AI modifies the file
    backup_path = file_path + ".bak"
    try:
        shutil.copy2(file_path, backup_path)
        print(f"Backup created at: {backup_path}")
    except Exception as e:
        print(f"Could not create backup: {e}")

    # Call the enhancer (full_prompt=None uses the standard prompt)
    result = enhance_test_method_with_ai(
        file_path=file_path,
        method_name=method_name,
        full_prompt=None,
        ai_provider=ai_provider
    )

    if result.get('success'):
        print("\nEnhancement succeeded.")
        print(f"File: {result['file_path']}")
        print(f"Method: {result['method_name']}")
        print(f"Provider: {result['ai_provider']}")
    else:
        print("\nEnhancement failed.")
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    main()
