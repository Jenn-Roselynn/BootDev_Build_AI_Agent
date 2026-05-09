import os

def get_files_info(working_directory, directory="."):
    """
    Lists files in a directory with size and type info, 
    wrapped in a security sandbox.
    """
    try:
        # 1. Normalize the sandbox root
        working_dir_abs = os.path.abspath(working_directory)
        
        # 2. Construct and normalize the target path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # 3. Security Check: Path Traversal Prevention
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # 4. Existence Check
        if not os.path.exists(target_dir):
            return f'Error: "{directory}" does not exist'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # 5. Build File Manifest
        items = os.listdir(target_dir)
        if not items:
            return f'Directory "{directory}" is empty'
            
        output_lines = []
        for item in items:
            item_path = os.path.join(target_dir, item)
            # Use os.lstat if you want to avoid following symlinks, 
            # but getsize is standard for this lesson.
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            output_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: {e}"

# OpenAI/Ollama Tool Specification
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (e.g., '.' for root or 'pkg' for a subdirectory)",
                },
            },
            "required": ["directory"],
        },
    },
}