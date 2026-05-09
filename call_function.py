from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

# The "Registry" of schemas for the LLM
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]

# The "Dispatcher" map for Python execution
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if we actually have this tool in our chest
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Prepare arguments
    args = dict(function_call.args) if function_call.args else {}
    # Force the working directory to our sandbox
    args["working_directory"] = "./calculator"

    # EXECUTION: The **args syntax unpacks the dict into keyword arguments
    function_logic = function_map[function_name]
    function_result = function_logic(**args)

    # Return the result wrapped in the specific Google GenAI tool format
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )