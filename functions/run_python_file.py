import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            
        if not result.stdout.strip() and not result.stderr.strip():
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")
                
        return "\n".join(output_parts)
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python script with optional command-line arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute."
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of string arguments to pass to the script."
                }
            },
            "required": ["file_path"]
        }
    }
}