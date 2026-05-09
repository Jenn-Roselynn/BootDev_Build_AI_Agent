import os

def search_code(working_directory, query, directory="."):
    """
    Searches for a string within all files in the sandbox.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return "Error: Search path is outside the permitted directory"

        results = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        if query in f.read():
                            # Return path relative to working directory
                            results.append(os.path.relpath(path, working_dir_abs))
                except:
                    continue
        return {"found_in": results} if results else "No matches found."
    except Exception as e:
        return f"Error: {e}"

schema_search_code = {
    "type": "function",
    "function": {
        "name": "search_code",
        "description": "Searches for a specific text string in all files within a directory tree.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The string to search for."},
                "directory": {"type": "string", "description": "The relative directory to start searching from (default '.')"}
            },
            "required": ["query"]
        }
    }
}