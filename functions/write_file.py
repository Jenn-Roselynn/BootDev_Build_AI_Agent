import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites content to a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path where the file should be written."
                },
                "content": {
                    "type": "string",
                    "description": "The full text content to write into the file."
                }
            },
            "required": ["file_path", "content"]
        }
    }
}