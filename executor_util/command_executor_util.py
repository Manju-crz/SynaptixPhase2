"""
Command Executor Utility - Reusable utility to execute PowerShell/system commands
"""

import subprocess
import os
import logging
from typing import Dict, Optional, List, Union

logger = logging.getLogger(__name__)


class CommandExecutor:
    """
    Utility class to execute system commands (PowerShell, pytest, etc.)
    """

    def __init__(self, working_directory: Optional[str] = None):
        """
        Initialize CommandExecutor

        Args:
            working_directory: Directory where commands will be executed (default: current directory)
        """
        self.working_directory = working_directory or os.getcwd()

    def execute_command(
        self,
        command: str,
        timeout: int = 300,
        capture_output: bool = True,
        shell: bool = True,
        env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Union[bool, str, int]]:
        """
        Execute a system command (PowerShell, pytest, etc.)

        Args:
            command: Command string to execute (e.g., "pytest .\\rest_test\\test8\\test8.py -v")
            timeout: Maximum execution time in seconds (default: 300 = 5 minutes)
            capture_output: Whether to capture stdout/stderr (default: True)
            shell: Whether to run command through shell (default: True for Windows)
            env: Optional environment variables dictionary

        Returns:
            Dictionary containing:
                - success (bool): True if command executed successfully (exit code 0)
                - command (str): The command that was executed
                - exit_code (int): Process exit code
                - stdout (str): Standard output
                - stderr (str): Standard error
                - message (str): Success/failure message
                - error (str, optional): Error details if exception occurred

        Example:
            >>> executor = CommandExecutor()
            >>> result = executor.execute_command("pytest .\\rest_test\\test8\\test8.py -v")
            >>> if result['success']:
            >>>     print(f"Test passed! Output: {result['stdout']}")
        """
        try:
            logger.info(f"Executing command: {command}")
            logger.info(f"Working directory: {self.working_directory}")

            # Set up environment variables - add PYTHONPATH for module imports
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
            
            # Add working directory to PYTHONPATH so pytest can find modules like rest_util
            if 'PYTHONPATH' in process_env:
                process_env['PYTHONPATH'] = f"{self.working_directory}{os.pathsep}{process_env['PYTHONPATH']}"
            else:
                process_env['PYTHONPATH'] = self.working_directory
            
            logger.info(f"PYTHONPATH set to: {process_env.get('PYTHONPATH')}")

            # Use Popen for better control and to prevent hanging in Flask/web contexts
            process = subprocess.Popen(
                command,
                shell=shell,
                cwd=self.working_directory,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                env=process_env
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                raise subprocess.TimeoutExpired(command, timeout, stdout, stderr)

            # Check if command was successful
            success = process.returncode == 0

            logger.info(f"Command completed with exit code: {process.returncode}")

            return {
                'success': success,
                'command': command,
                'exit_code': process.returncode,
                'stdout': stdout if capture_output and stdout else '',
                'stderr': stderr if capture_output and stderr else '',
                'message': 'Command executed successfully' if success else f'Command failed with exit code {process.returncode}'
            }

        except subprocess.TimeoutExpired as e:
            error_msg = f'Command timed out after {timeout} seconds'
            logger.error(error_msg)
            return {
                'success': False,
                'command': command,
                'exit_code': -1,
                'stdout': e.stdout if hasattr(e, 'stdout') and e.stdout else '',
                'stderr': e.stderr if hasattr(e, 'stderr') and e.stderr else '',
                'message': error_msg,
                'error': str(e)
            }

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            error_msg = f'Failed to execute command: {str(e)}'
            logger.error(error_msg)
            logger.error(error_trace)

            return {
                'success': False,
                'command': command,
                'exit_code': -1,
                'stdout': '',
                'stderr': '',
                'message': error_msg,
                'error': error_trace
            }
        
    def execute_pytest_command(
        self,
        pytest_command: str,
        timeout: int = 300
    ) -> Dict[str, Union[bool, str, int]]:
        """
        Execute a pytest command specifically

        Args:
            pytest_command: Full pytest command string
            timeout: Maximum execution time in seconds (default: 300)

        Returns:
            Dictionary with execution results (same as execute_command)

        Example:
            >>> executor = CommandExecutor()
            >>> result = executor.execute_pytest_command(
            >>>     "pytest .\\rest_test\\test8\\test8.py::TestGeneratedAPIs::test_01_create_a_new_pet_ai -v -s"
            >>> )
        """
        logger.info(f"Executing pytest command: {pytest_command}")
        return self.execute_command(
            command=pytest_command,
            timeout=timeout,
            capture_output=True,
            shell=True
        )

    def execute_powershell_script(
        self,
        script_path: str,
        arguments: Optional[List[str]] = None,
        timeout: int = 300
    ) -> Dict[str, Union[bool, str, int]]:
        """
        Execute a PowerShell script file

        Args:
            script_path: Path to PowerShell script (.ps1 file)
            arguments: Optional list of arguments to pass to the script
            timeout: Maximum execution time in seconds

        Returns:
            Dictionary with execution results

        Example:
            >>> executor = CommandExecutor()
            >>> result = executor.execute_powershell_script("deploy.ps1", ["-Environment", "Production"])
        """
        args_str = ' '.join(arguments) if arguments else ''
        command = f'powershell -ExecutionPolicy Bypass -File "{script_path}" {args_str}'

        logger.info(f"Executing PowerShell script: {script_path}")
        return self.execute_command(
            command=command,
            timeout=timeout,
            capture_output=True,
            shell=True
        )

    def execute_generated_test_interactive(self) -> Dict[str, Union[bool, str, int]]:
        """
        Interactive method to execute a generated test by asking for folder and file name
        Uses command_builder_util to build the pytest command

        Returns:
            Dictionary with execution results

        Example:
            >>> executor = CommandExecutor()
            >>> result = executor.execute_generated_test_interactive()
            # User will be prompted for folder name, file name, and timeout
        """
        from executor_util.command_builder_util import build_pytest_command

        print("\n" + "="*80)
        print("🚀 Execute Generated Test (Interactive Mode)")
        print("="*80)

        # Get folder name from user
        print("\n📁 Enter the test folder name (e.g., test8, test10)")
        folder_name = input("Folder name: ").strip()

        if not folder_name:
            return {
                'success': False,
                'command': '',
                'exit_code': -1,
                'stdout': '',
                'stderr': '',
                'message': 'Folder name cannot be empty',
                'error': 'User provided empty folder name'
            }

        # Get file name from user
        print("\n📄 Enter the test file name without .py extension (e.g., test8, test10)")
        file_name = input("File name: ").strip()

        if not file_name:
            return {
                'success': False,
                'command': '',
                'exit_code': -1,
                'stdout': '',
                'stderr': '',
                'message': 'File name cannot be empty',
                'error': 'User provided empty file name'
            }

        # Validate that the test file exists
        test_file_path = os.path.join(self.working_directory, "rest_test", folder_name, f"{file_name}.py")

        if not os.path.exists(test_file_path):
            error_msg = f"Test file not found at: {test_file_path}"
            print(f"\n❌ Error: {error_msg}")
            print("Please check that the folder and file name are correct.")
            return {
                'success': False,
                'command': '',
                'exit_code': -1,
                'stdout': '',
                'stderr': '',
                'message': 'Test file not found',
                'error': error_msg
            }

        print(f"\n✅ Test file found: {test_file_path}")

        # Get timeout (optional)
        timeout_input = input("\n⏱️  Enter timeout in seconds (default: 300): ").strip()
        timeout = 300
        if timeout_input:
            try:
                timeout = int(timeout_input)
            except ValueError:
                print("⚠️ Invalid timeout, using default 300 seconds")
                timeout = 300

        print("\n" + "="*80)
        print("🔨 Building pytest command...")
        print("="*80)

        # Build pytest command using command_builder_util
        pytest_command = build_pytest_command(folder_name, file_name)

        if not pytest_command:
            error_msg = "Failed to build pytest command. Make sure the test file contains a test class and AI-modified test method (_ai suffix)"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'command': '',
                'exit_code': -1,
                'stdout': '',
                'stderr': '',
                'message': 'Failed to build pytest command',
                'error': error_msg
            }

        print(f"✅ Command built successfully!")
        print(f"📜 Command: {pytest_command}")

        print("\n" + "="*80)
        print("⏳ Executing pytest command...")
        print("="*80)
        print(f"📁 Working Dir: {self.working_directory}")
        print(f"⏱️  Timeout: {timeout}s")
        print()

        # Execute the command
        result = self.execute_pytest_command(pytest_command, timeout=timeout)

        # Display results
        print("\n" + "="*80)
        print("📊 Execution Results")
        print("="*80)
        print(f"✔️ Success: {result['success']}")
        print(f"🔢 Exit Code: {result['exit_code']}")
        print(f"📝 Message: {result['message']}")

        if result['stdout']:
            print("\n" + "-"*80)
            print("📤 STDOUT:")
            print("-"*80)
            # Show last 2000 characters to avoid overwhelming output
            stdout = result['stdout']
            if len(stdout) > 2000:
                print(f"... (showing last 2000 characters of {len(stdout)} total)")
                print(stdout[-2000:])
            else:
                print(stdout)

        if result['stderr']:
            print("\n" + "-"*80)
            print("⚠️ STDERR:")
            print("-"*80)
            # Show last 1000 characters
            stderr = result['stderr']
            if len(stderr) > 1000:
                print(f"... (showing last 1000 characters of {len(stderr)} total)")
                print(stderr[-1000:])
            else:
                print(stderr)

        if 'error' in result:
            print("\n" + "-"*80)
            print("❌ ERROR:")
            print("-"*80)
            print(result['error'][:500] if len(result['error']) > 500 else result['error'])

        print("\n" + "="*80)

        return result


def execute_command(
    command: str,
    working_directory: Optional[str] = None,
    timeout: int = 300
) -> Dict[str, Union[bool, str, int]]:
    """
    Convenience function to execute a command without creating CommandExecutor instance

    Args:
        command: Command string to execute
        working_directory: Directory where command will be executed
        timeout: Maximum execution time in seconds

    Returns:
        Dictionary with execution results

    Example:
        >>> from executor_util.command_executor_util import execute_command
        >>> result = execute_command("pytest .\\rest_test\\test8\\test8.py -v")
        >>> print(result['stdout'])
    """
    executor = CommandExecutor(working_directory)
    return executor.execute_command(command, timeout=timeout)
        