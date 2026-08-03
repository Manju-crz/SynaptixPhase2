"""
Command Builder Utility - Interactive pytest command builder for single test folder/file
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from executor_util.command_builder_util import build_pytest_command


def build_command_interactive():
    """
    Build pytest command from interactive user input for a single folder/file
    """
    print("\n" + "="*80)
    print("🚀 Building Pytest Command")
    print("="*80)

    # Get folder name from user
    folder_name = input("\n📁 Enter test folder name (e.g., test8): ").strip()
    if not folder_name:
        print("❌ Folder name cannot be empty")
        return None

    # Validate folder exists before asking for file name
    folder_path = os.path.join(os.getcwd(), "rest_test", folder_name)
    if not os.path.exists(folder_path):
        print(f"\n❌ Error: Test folder '{folder_name}' does not exist!")
        print(f"   Expected path: {folder_path}")
        print(f"\n💡 Available test folders:")
        rest_test_path = os.path.join(os.getcwd(), "rest_test")
        if os.path.exists(rest_test_path):
            folders = [f for f in os.listdir(rest_test_path) if os.path.isdir(os.path.join(rest_test_path, f)) and not f.startswith('_')]
            if folders:
                for f in sorted(folders):
                    print(f"   - {f}")
            else:
                print("   (No test folders found)")
        return None

    # Get file name from user
    file_name = input("📄 Enter test file name without .py (e.g., test8): ").strip()
    if not file_name:
        print("❌ File name cannot be empty")
        return None

    # Validate file exists
    file_path = os.path.join(folder_path, f"{file_name}.py")
    if not os.path.exists(file_path):
        print(f"\n❌ Error: Test file '{file_name}.py' does not exist in folder '{folder_name}'!")
        print(f"   Expected path: {file_path}")
        print(f"\n💡 Available files in {folder_name}:")
        files = [f for f in os.listdir(folder_path) if f.endswith('.py') and not f.startswith('_')]
        if files:
            for f in sorted(files):
                print(f"   - {f}")
        else:
            print("   (No Python files found)")
        return None

    print(f"\n🔍 Building command for: {folder_name}/{file_name}.py")

    command = build_pytest_command(folder_name, file_name)

    if command:
        print(f"\n✅ Command built successfully:\n")
        print(f"   {command}\n")
        print("="*80)
        print("📋 Copy and run this command:")
        print("="*80)
        print(command)
        print("="*80)
        return command
    else:
        print("\n❌ Failed to build command")
        print("   - Check if the test file exists")
        print("   - Verify the file contains a test class starting with 'Test'")
        print("   - Ensure there's a test method ending with '_ai'")
        return None


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 Command Builder Utility")
    print("="*80)
    print("\nBuild pytest command for a single test folder and file")

    try:
        build_command_interactive()

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

        