import os

def get_project_tree(working_directory):
    """
    Provides a visual tree of the entire project structure.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        tree = []
        
        for root, dirs, files in os.walk(working_dir_abs):
            # Ignore hidden/junk folders
            dirs[:] = [d for d in dirs if not d.startswith(('.', '__'))]
            
            level = os.path.relpath(root, working_dir_abs).count(os.sep)
            if root == working_dir_abs:
                level = 0
            
            indent = " " * 4 * level
            tree.append(f"{indent}{os.path.basename(root)}/")
            
            sub_indent = " " * 4 * (level + 1)
            for f in files:
                if not f.startswith('.'):
                    tree.append(f"{sub_indent}{f}")
                    
        return "\n".join(tree)
    except Exception as e:
        return f"Error: {e}"

schema_get_project_tree = {
    "type": "function",
    "function": {
        "name": "get_project_tree",
        "description": "Returns a visual-style text tree of the entire project file structure.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}