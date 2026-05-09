import os
import subprocess

def run_shell_command(working_directory, command):
    """
    Executes a bash/cmd command within the sandbox.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        # Note: Shell execution is powerful. We keep it inside the working_dir.
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = []
        if result.stdout: output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr: output.append(f"STDERR:\n{result.stderr}")
        if not output: output.append("Command executed with no output.")
        
        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"

schema_run_shell_command = {
    "type": "function",
    "function": {
        "name": "run_shell_command",
        "description": "Executes a shell command (like 'ls', 'pip list', or 'pytest') in the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The full command string to execute."}
            },
            "required": ["command"]
        }
    }
}
