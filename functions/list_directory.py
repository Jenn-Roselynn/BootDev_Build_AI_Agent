import os

def list_directory(directory="."):
    """
    Lists files and folders in a directory to help the agent navigate.
    """
    try:
        items = os.listdir(directory)
        # Filter out noise like __pycache__ or .git
        ignored = {"__pycache__", ".git", ".venv", ".ruff_cache"}
        filtered_items = [item for item in items if item not in ignored]
        return {"items": filtered_items}
    except Exception as e:
        return {"error": str(e)}