"""
Example usage of Command Executor Utility
Demonstrates how to execute system commands, pytest commands, and PowerShell scripts
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from executor_util.command_executor_util import CommandExecutor, execute_command


def example_1_simple_command():
    """
    Example 1: Execute a simple system command
    """
    print("="*80)
    print("EXAMPLE 1: Simple System Command")
    print("="*80)

    # Execute a simple dir/ls command
    result = execute_command("dir" if os.name == 'nt' else "ls")

    print(f"\n✅ Success: {result['success']}")
    print(f"📜 Command: {result['command']}")
    print(f"🔢 Exit Code: {result['exit_code']}")
    print(f"📝 Message: {result['message']}")
    print(f"\n--- Output (first 500 chars) ---")
    print(result['stdout'][:500])


def example_2_pytest_command():
    """
    Example 2: Execute a pytest command
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Execute Pytest Command")
    print("="*80)

    # Create executor with project root as working directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    executor = CommandExecutor(working_directory=project_root)

    # Execute pytest command
    pytest_command = "pytest .\\rest_test\\test8\\test8.py::TestGeneratedAPIs::test_01_create_a_new_pet_ai -v -s --alluredir=allure-results"

    print(f"\n🔍 Executing: {pytest_command}")
    print("⏳ This may take a few seconds...\n")

    result = executor.execute_pytest_command(pytest_command, timeout=60)

    print(f"\n✅ Success: {result['success']}")
    print(f"🔢 Exit Code: {result['exit_code']}")
    print(f"📝 Message: {result['message']}")

    if result['success']:
        print("\n✅ Test passed!")
        print(f"--- Output (last 500 chars) ---")
        print(result['stdout'][-500:])
    else:
        print("\n❌ Test failed!")
        print(f"--- Error Output ---")
        print(result['stderr'][:500] if result['stderr'] else "No stderr")


def example_3_command_with_timeout():
    """
    Example 3: Execute command with custom timeout
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Command with Custom Timeout")
    print("="*80)

    executor = CommandExecutor()

    # Execute a command with short timeout (will succeed quickly)
    result = executor.execute_command(
        command="echo Hello World",
        timeout=5
    )

    print(f"\n✅ Success: {result['success']}")
    print(f"📜 Command: {result['command']}")
    print(f"📝 Output: {result['stdout'].strip()}")


def example_4_command_class_usage():
    """
    Example 4: Using CommandExecutor class with different working directories
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: CommandExecutor Class with Working Directory")
    print("="*80)

    # Create executor with specific working directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    executor = CommandExecutor(working_directory=project_root)

    print(f"\n📁 Working Directory: {executor.working_directory}")

    # Execute command in that directory
    result = executor.execute_command("dir" if os.name == 'nt' else "ls")

    print(f"\n✅ Success: {result['success']}")
    print(f"📝 Files in directory (first 300 chars):")
    print(result['stdout'][:300])


def example_5_error_handling():
    """
    Example 5: Error handling with invalid command
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Error Handling")
    print("="*80)

    executor = CommandExecutor()

    # Try to execute an invalid command
    result = executor.execute_command("invalid_command_that_does_not_exist")

    print(f"\n❌ Success: {result['success']}")
    print(f"📜 Command: {result['command']}")
    print(f"🔢 Exit Code: {result['exit_code']}")
    print(f"📝 Message: {result['message']}")

    if 'error' in result:
        print(f"\n⚠️ Error Details:")
        print(result['error'][:300])


def example_6_powershell_script():
    """
    Example 6: Execute PowerShell script (Windows only)
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: PowerShell Script Execution")
    print("="*80)

    if os.name != 'nt':
        print("\n⚠️ Skipped - PowerShell scripts are Windows-only")
        return

    executor = CommandExecutor()

    # Execute a simple PowerShell command
    result = executor.execute_command(
        'powershell -Command "Get-Date; Write-Host \'Hello from PowerShell!\'"'
    )

    print(f"\n✅ Success: {result['success']}")
    print(f"📝 Output:")
    print(result['stdout'])


def example_7_convenience_function():
    """
    Example 7: Using convenience function without creating class instance
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Convenience Function")
    print("="*80)

    # Use the convenience function directly
    result = execute_command(
        command="echo Testing convenience function",
        timeout=10
    )

    print(f"\n✅ Success: {result['success']}")
    print(f"📝 Output: {result['stdout'].strip()}")


def example_8_check_python_version():
    """
    Example 8: Check Python version using command executor
    """
    print("\n" + "="*80)
    print("EXAMPLE 8: Check Python Version")
    print("="*80)

    result = execute_command("python --version")

    print(f"\n✅ Success: {result['success']}")
    print(f"🐍 Python Version: {result['stdout'].strip()}")


def run_custom_command():
    """
    Interactive mode: Execute pytest test by providing folder and file name
    Uses the reusable method from CommandExecutor class
    """
    # Get project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create executor with project root as working directory
    executor = CommandExecutor(working_directory=project_root)

    # Call the reusable interactive method
    result = executor.execute_generated_test_interactive()

    # Result is already displayed by the method, just return
    return result


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 Command Executor Utility")
    print("="*80)

    try:
        # Show menu
        print("\nChoose an option:")
        print("  1. Execute generated test (folder/file input)")
        print("  2. Run all examples")
        print("  3. Exit")

        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            # Interactive custom command mode
            run_custom_command()

        elif choice == "2":
            # Run all examples
            print("\n🚀 Running All Examples\n")

            example_1_simple_command()
            example_3_command_with_timeout()
            example_4_command_class_usage()
            example_5_error_handling()
            example_6_powershell_script()
            example_7_convenience_function()
            example_8_check_python_version()

            # Pytest example (commented out by default as it requires actual test file)
            print("\n" + "="*80)
            print("⚠️  EXAMPLE 2 (Pytest) - Skipped by default")
            print("="*80)
            print("Uncomment example_2_pytest_command() to run pytest tests")
            print("Make sure test8/test8.py exists with AI-modified test method")
            # example_2_pytest_command()

            print("\n" + "="*80)
            print("✅ All examples completed!")
            print("="*80)

        elif choice == "3":
            print("\n👋 Goodbye!")

        else:
            print("\n❌ Invalid choice. Please run the script again and choose 1, 2, or 3.")

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()