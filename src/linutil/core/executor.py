"""
Command Executor Module

Handles command execution with sudo support, output parsing, and error handling.
"""

import asyncio
import shutil
import re
from dataclasses import dataclass
from typing import Optional, Callable, Any
from enum import Enum


class CommandStatus(Enum):
    """Status of command execution."""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class CommandResult:
    """Result of command execution."""
    
    command: str
    return_code: int
    stdout: str
    stderr: str
    status: CommandStatus
    execution_time: float = 0.0
    
    @property
    def success(self) -> bool:
        """Check if command succeeded."""
        return self.return_code == 0 and self.status == CommandStatus.SUCCESS
    
    @property
    def output(self) -> str:
        """Get combined output."""
        return self.stdout + self.stderr


class PrivilegeError(Exception):
    """Raised when privilege elevation fails."""
    pass


class PrivilegeHandler:
    """Handles privilege elevation (sudo)."""
    
    def __init__(self):
        self.has_sudo = shutil.which("sudo") is not None
        self.has_pkexec = shutil.which("pkexec") is not None
        self._privileges_cached = False
    
    def can_elevate(self) -> bool:
        """Check if we can elevate privileges."""
        return self.has_sudo or self.has_pkexec
    
    async def check_privileges(self) -> bool:
        """
        Check if we currently have cached sudo privileges.
        
        Returns:
            True if we have cached privileges
        """
        if not self.has_sudo:
            return False
        
        try:
            process = await asyncio.create_subprocess_exec(
                "sudo", "-n", "true",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await process.wait()
            self._privileges_cached = (process.returncode == 0)
            return self._privileges_cached
        except Exception:
            return False
    
    async def request_elevation(self) -> bool:
        """
        Request privilege elevation (will prompt for password).
        
        Returns:
            True if elevation succeeded
            
        Raises:
            PrivilegeError: If elevation fails
        """
        if not self.can_elevate():
            raise PrivilegeError("No privilege elevation tool found (sudo/pkexec)")
        
        try:
            # Request sudo with a simple true command
            process = await asyncio.create_subprocess_exec(
                "sudo", "true",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            if process.returncode == 0:
                self._privileges_cached = True
                return True
            else:
                raise PrivilegeError("Privilege elevation was denied")
                
        except Exception as e:
            raise PrivilegeError(f"Failed to elevate privileges: {e}")
    
    def wrap_command(self, command: str, use_sudo: bool = False) -> str:
        """
        Wrap command with sudo if needed.
        
        Args:
            command: Command to wrap
            use_sudo: Whether to use sudo
            
        Returns:
            Wrapped command
        """
        if use_sudo and self.has_sudo:
            # Use -S to read password from stdin if needed
            # Use -E to preserve environment variables
            return f"sudo -n {command}"
        return command


class CommandExecutor:
    """Executes shell commands with various options."""
    
    def __init__(self, privilege_handler: Optional[PrivilegeHandler] = None):
        """
        Initialize command executor.
        
        Args:
            privilege_handler: Handler for privilege elevation
        """
        self.privilege_handler = privilege_handler or PrivilegeHandler()
    
    async def execute(
        self,
        command: str,
        use_sudo: bool = False,
        timeout: Optional[float] = None,
        on_output: Optional[Callable[[str], None]] = None,
        env: Optional[dict[str, str]] = None
    ) -> CommandResult:
        """
        Execute a shell command.
        
        Args:
            command: Command to execute
            use_sudo: Whether to use sudo
            timeout: Timeout in seconds (None for no timeout)
            on_output: Callback for real-time output (receives each line)
            env: Environment variables to set
            
        Returns:
            CommandResult with execution details
            
        Raises:
            PrivilegeError: If sudo is required but not available
        """
        import time
        start_time = time.time()
        
        # Wrap with sudo if needed
        if use_sudo:
            if not self.privilege_handler.can_elevate():
                raise PrivilegeError("Sudo required but not available")
            
            # Check if we have cached privileges
            has_privs = await self.privilege_handler.check_privileges()
            if not has_privs:
                # Request elevation
                await self.privilege_handler.request_elevation()
            
            command = self.privilege_handler.wrap_command(command, use_sudo=True)
        
        # Set up environment
        import os
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)
        
        # Force non-interactive mode for package managers
        exec_env.update({
            "DEBIAN_FRONTEND": "noninteractive",
            "NEEDRESTART_MODE": "a",  # Restart services automatically
            "LANG": "C",  # English output for parsing
            "LC_ALL": "C",
        })
        
        try:
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=exec_env
            )
            
            # Collect output
            stdout_lines: list[str] = []
            stderr_lines: list[str] = []
            
            async def read_stream(stream: asyncio.StreamReader, lines_list: list[str]):
                """Read from stream line by line."""
                while True:
                    try:
                        line = await stream.readline()
                        if not line:
                            break
                        decoded = line.decode('utf-8', errors='replace')
                        lines_list.append(decoded)
                        
                        if on_output:
                            on_output(decoded.rstrip())
                    except Exception:
                        break
            
            # Read both streams concurrently
            if timeout:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(
                            read_stream(process.stdout, stdout_lines),
                            read_stream(process.stderr, stderr_lines)
                        ),
                        timeout=timeout
                    )
                    await asyncio.wait_for(process.wait(), timeout=1.0)
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    
                    execution_time = time.time() - start_time
                    return CommandResult(
                        command=command,
                        return_code=-1,
                        stdout=''.join(stdout_lines),
                        stderr=''.join(stderr_lines),
                        status=CommandStatus.TIMEOUT,
                        execution_time=execution_time
                    )
            else:
                await asyncio.gather(
                    read_stream(process.stdout, stdout_lines),
                    read_stream(process.stderr, stderr_lines)
                )
                await process.wait()
            
            execution_time = time.time() - start_time
            
            return CommandResult(
                command=command,
                return_code=process.returncode,
                stdout=''.join(stdout_lines),
                stderr=''.join(stderr_lines),
                status=CommandStatus.SUCCESS if process.returncode == 0 else CommandStatus.FAILED,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return CommandResult(
                command=command,
                return_code=-1,
                stdout="",
                stderr=str(e),
                status=CommandStatus.FAILED,
                execution_time=execution_time
            )
    
    async def execute_multiple(
        self,
        commands: list[str],
        use_sudo: bool = False,
        stop_on_error: bool = True,
        on_command_start: Optional[Callable[[str], None]] = None,
        on_command_complete: Optional[Callable[[CommandResult], None]] = None
    ) -> list[CommandResult]:
        """
        Execute multiple commands in sequence.
        
        Args:
            commands: List of commands to execute
            use_sudo: Whether to use sudo
            stop_on_error: Stop if a command fails
            on_command_start: Callback when command starts
            on_command_complete: Callback when command completes
            
        Returns:
            List of CommandResults
        """
        results: list[CommandResult] = []
        
        for cmd in commands:
            if on_command_start:
                on_command_start(cmd)
            
            result = await self.execute(cmd, use_sudo=use_sudo)
            results.append(result)
            
            if on_command_complete:
                on_command_complete(result)
            
            if stop_on_error and not result.success:
                break
        
        return results


def parse_package_manager_output(output: str, package_manager: str) -> dict[str, Any]:
    """
    Parse package manager output to extract progress information.
    
    Args:
        output: Raw output from package manager
        package_manager: Type of package manager (apt, dnf, etc.)
        
    Returns:
        Dictionary with parsed information
    """
    info: dict[str, Any] = {
        "progress": None,
        "current_action": "",
        "packages_total": 0,
        "packages_done": 0
    }
    
    if package_manager == "apt":
        # Look for progress indicators
        progress_match = re.search(r'Progress:\s*\[(\d+)%\]', output)
        if progress_match:
            info["progress"] = int(progress_match.group(1))
        
        # Look for package actions
        if "Reading package lists" in output:
            info["current_action"] = "Reading package lists"
        elif "Building dependency tree" in output:
            info["current_action"] = "Building dependency tree"
        elif "Unpacking" in output:
            info["current_action"] = "Unpacking packages"
        elif "Setting up" in output:
            info["current_action"] = "Setting up packages"
        elif "Processing triggers" in output:
            info["current_action"] = "Processing triggers"
    
    elif package_manager == "dnf":
        # DNF progress patterns
        if "Downloading Packages:" in output:
            info["current_action"] = "Downloading packages"
        elif "Installing" in output:
            info["current_action"] = "Installing"
        elif "Running transaction check" in output:
            info["current_action"] = "Checking transaction"
        elif "Running transaction test" in output:
            info["current_action"] = "Testing transaction"
    
    return info


if __name__ == "__main__":
    # Test the executor
    async def test():
        executor = CommandExecutor()
        
        print("Testing simple command...")
        result = await executor.execute("echo 'Hello, World!'")
        print(f"Result: {result.stdout.strip()}")
        print(f"Success: {result.success}")
        
        print("\nTesting command with output callback...")
        def output_callback(line: str):
            print(f"  > {line}")
        
        result = await executor.execute(
            "echo 'Line 1' && echo 'Line 2' && echo 'Line 3'",
            on_output=output_callback
        )
        
        print("\nTesting multiple commands...")
        results = await executor.execute_multiple([
            "echo 'First command'",
            "echo 'Second command'",
            "echo 'Third command'"
        ])
        print(f"Executed {len(results)} commands")
    
    asyncio.run(test())
