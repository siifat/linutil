"""
Terminal Executor Module

Handles interactive terminal command execution with user input support.
"""

import subprocess
import sys
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class TerminalResult:
    """Result of terminal command execution."""
    
    return_code: int
    success: bool
    
    @staticmethod
    def from_code(code: int) -> 'TerminalResult':
        """Create result from return code."""
        return TerminalResult(return_code=code, success=(code == 0))


class TerminalExecutor:
    """
    Executes commands in an interactive terminal session.
    
    This allows users to see real-time output and provide input
    (passwords, confirmations, etc.) during command execution.
    """
    
    def __init__(self):
        """Initialize terminal executor."""
        self.shell = self._detect_shell()
    
    def _detect_shell(self) -> str:
        """Detect the user's shell."""
        import os
        return os.environ.get('SHELL', '/bin/bash')
    
    def execute_interactive(
        self,
        commands: List[str],
        use_sudo: bool = False,
        description: Optional[str] = None
    ) -> TerminalResult:
        """
        Execute commands interactively in the user's terminal.
        
        This function will run the commands and allow full user interaction
        including password prompts, confirmations, and viewing output.
        
        Args:
            commands: List of commands to execute
            use_sudo: Whether to use sudo (will prompt for password)
            description: Optional description to show before execution
            
        Returns:
            TerminalResult with return code and success status
        """
        # Create a shell script to execute
        script_lines = ["#!/bin/bash", "set -e"]  # Exit on error
        
        if description:
            script_lines.append(f'echo "==================================="')
            script_lines.append(f'echo "{description}"')
            script_lines.append(f'echo "==================================="')
            script_lines.append('echo ""')
        
        # Add commands
        for cmd in commands:
            if use_sudo and not cmd.strip().startswith('sudo'):
                script_lines.append(f'sudo {cmd}')
            else:
                script_lines.append(cmd)
        
        # Add completion message
        script_lines.append('echo ""')
        script_lines.append('echo "==================================="')
        script_lines.append('echo "Operation completed!"')
        script_lines.append('echo "==================================="')
        script_lines.append('echo ""')
        script_lines.append('read -p "Press Enter to continue..."')
        
        script_content = '\n'.join(script_lines)
        
        # Execute in the current terminal
        try:
            result = subprocess.run(
                ['bash', '-c', script_content],
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=False
            )
            return TerminalResult.from_code(result.returncode)
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return TerminalResult.from_code(130)  # SIGINT
        
        except Exception as e:
            print(f"\n\nError executing command: {e}")
            return TerminalResult.from_code(1)
    
    def execute_with_confirmation(
        self,
        commands: List[str],
        use_sudo: bool = False,
        description: Optional[str] = None,
        warning: Optional[str] = None
    ) -> TerminalResult:
        """
        Execute commands with user confirmation.
        
        Args:
            commands: List of commands to execute
            use_sudo: Whether to use sudo
            description: Description of what will be done
            warning: Optional warning message
            
        Returns:
            TerminalResult with return code and success status
        """
        # Show what will be executed
        print("\n" + "=" * 60)
        if description:
            print(f"{description}")
        print("=" * 60)
        
        print("\nThe following commands will be executed:\n")
        for i, cmd in enumerate(commands, 1):
            prefix = "sudo " if use_sudo and not cmd.strip().startswith('sudo') else ""
            print(f"  {i}. {prefix}{cmd}")
        
        if warning:
            print(f"\n⚠️  WARNING: {warning}")
        
        print("\n" + "=" * 60)
        
        # Ask for confirmation
        try:
            response = input("\nContinue? [y/N]: ").strip().lower()
            if response not in ['y', 'yes']:
                print("Operation cancelled.")
                return TerminalResult.from_code(0)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return TerminalResult.from_code(130)
        
        # Execute
        return self.execute_interactive(commands, use_sudo, description)


if __name__ == "__main__":
    # Test the executor
    executor = TerminalExecutor()
    
    print("Testing interactive execution...")
    result = executor.execute_interactive(
        commands=['echo "Hello from terminal!"', 'whoami'],
        description="Test Command Execution"
    )
    print(f"Result: {'Success' if result.success else 'Failed'} (code: {result.return_code})")
    
    print("\nTesting with confirmation...")
    result = executor.execute_with_confirmation(
        commands=['date', 'uptime'],
        description="Show System Information",
        warning="This is just a test"
    )
    print(f"Result: {'Success' if result.success else 'Failed'} (code: {result.return_code})")
