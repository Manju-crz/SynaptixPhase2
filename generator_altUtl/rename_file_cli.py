"""
Command-Line File Rename Utility
Simple CLI tool to rename test files in rest_test folders.

Usage:
    python rename_file_cli.py <folder_name> <existing_file_name> <new_file_name>

Examples:
    python rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest
    python rename_file_cli.py TestComponent_01 TestFile_01.py CreatePetTest.py
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator_altUtl.file_rename_util import rename_file_in_folder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_usage():
    """Print usage instructions"""
    print("\n" + "="*70)
    print("FILE RENAME UTILITY - Command Line Interface")
    print("="*70)
    print("\nUsage:")
    print("  python rename_file_cli.py <folder_name> <existing_file> <new_file>")
    print("\nArguments:")
    print("  folder_name     - Name of the folder containing the file (e.g., TestComponent_01)")
    print("  existing_file   - Current file name (with or without .py extension)")
    print("  new_file        - New file name (with or without .py extension)")
    print("\nExamples:")
    print("  python rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest")
    print("  python rename_file_cli.py TestComponent_01 TestFile_01.py CreatePetTest.py")
    print("  python rename_file_cli.py TestComponent_01 old_test new_test")
    print("\n" + "="*70 + "\n")


def main():
    """Main function to handle command-line file renaming"""
    
    # Check if correct number of arguments provided
    if len(sys.argv) != 4:
        print("\n❌ Error: Incorrect number of arguments!")
        print_usage()
        sys.exit(1)
    
    # Extract arguments
    folder_name = sys.argv[1]
    existing_file_name = sys.argv[2]
    new_file_name = sys.argv[3]
    
    print("\n" + "="*70)
    print("FILE RENAME OPERATION")
    print("="*70)
    print(f"\n📁 Folder:        {folder_name}")
    print(f"📄 Existing File: {existing_file_name}")
    print(f"✨ New File:      {new_file_name}")
    print("\n" + "-"*70)
    
    # Get project root (parent of generator_altUtl)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n🔍 Searching in:  {project_root}")
    
    # Call the rename utility
    print("\n⏳ Processing...")
    result = rename_file_in_folder(
        folder_name=folder_name,
        existing_file_name=existing_file_name,
        new_file_name=new_file_name,
        project_root=project_root,
        search_recursive=True
    )
    
    # Display results
    print("\n" + "="*70)
    if result['success']:
        print("✅ SUCCESS!")
        print("="*70)
        print(f"\n{result['message']}")
        print(f"\n📂 Old Path: {result['old_file_path']}")
        print(f"📂 New Path: {result['new_file_path']}")
        print("\n" + "="*70 + "\n")
        sys.exit(0)
    else:
        print("❌ FAILED!")
        print("="*70)
        print(f"\n{result['message']}")
        print("\n" + "="*70 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}\n")
        logger.exception("Unexpected error occurred")
        sys.exit(1)
