#!/usr/bin/env python3
import os
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
import config

# 1. Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")

# 2. Simulated Google GenAI types for Boot.dev compatibility
class types:
    class Part:
        def __init__(self, text=None, function_call=None, function_response=None):
            self.text = text
            self.function_call = function_call
            self.function_response = function_response

    class Content:
        def __init__(self, role, parts):
            self.role = role
            self.parts = parts
            
    class FunctionCall:
        def __init__(self, name, args, call_id=None):
            self.name = name
            self.args = args
            self.call_id = call_id

def main():
    # 3. Setup Argument Parsing
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # 4. Initialize Conversation History
    messages = [
        types.Content(role="system", parts=[types.Part(text=system_prompt)]),
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # 5. Initialize Local Ollama Client
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    # 6. THE AGENT LOOP
    for i in range(20):
        ollama_messages = []
        for turn_idx, m in enumerate(messages):
            if any(p.function_response for p in m.parts):
                # This turn contains tool responses; map them to the OpenAI 'tool' role
                for p in m.parts:
                    if p.function_response:
                        ollama_messages.append({
                            "role": "tool",
                            "tool_call_id": p.function_response.get("id", f"call_{turn_idx}"),
                            "content": json.dumps(str(p.function_response.get("response", "")))
                        })
            else:
                msg_dict = {"role": m.role}
                content_text = ""
                tool_calls = []
                
                for p_idx, p in enumerate(m.parts):
                    if p.text:
                        content_text += p.text
                    if p.function_call:
                        call_id = getattr(p.function_call, 'call_id', None) or f"call_{turn_idx}_{p_idx}"
                        tool_calls.append({
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": p.function_call.name,
                                "arguments": json.dumps(p.function_call.args)
                            }
                        })
                
                msg_dict["content"] = content_text if content_text else None
                if tool_calls:
                    msg_dict["tool_calls"] = tool_calls
                ollama_messages.append(msg_dict)

        try:
            response = client.chat.completions.create(
                model=config.MODEL,
                messages=ollama_messages,
                tools=available_functions,
                temperature=0
            )
        except Exception as e:
            print(f"Error calling the model: {e}")
            sys.exit(1)

        message = response.choices[0].message
        
        # 7. CAPTURE TOOL CALLS (Official or Text-Fallback)
        actual_tool_calls = message.tool_calls
        
        if not actual_tool_calls and message.content and '{"name":' in message.content:
            try:
                start_idx = message.content.find('{')
                end_idx = message.content.rfind('}') + 1
                json_str = message.content[start_idx:end_idx]
                tool_data = json.loads(json_str)
                
                class MockFunction:
                    def __init__(self, name, args, call_id):
                        self.name = name
                        self.arguments = json.dumps(args)
                        self.id = call_id

                class MockTool:
                    def __init__(self, d, call_id):
                        self.id = call_id
                        self.function = MockFunction(d['name'], d.get('args') or d.get('arguments'), call_id)
                
                actual_tool_calls = [MockTool(tool_data, f"call_{i}_fallback")]
            except Exception:
                pass

        current_parts = [types.Part(text=message.content)]
        if actual_tool_calls:
            for tc in actual_tool_calls:
                current_parts.append(types.Part(
                    function_call=types.FunctionCall(
                        tc.function.name, 
                        json.loads(tc.function.arguments), 
                        call_id=tc.id
                    )
                ))
        
        messages.append(types.Content(role="assistant", parts=current_parts))

        # 8. EXECUTE TOOLS
        if actual_tool_calls:
            function_responses = []
            for tool_call in actual_tool_calls:
                fc_args = json.loads(tool_call.function.arguments)
                
                # --- NEW FIX: Handle Newline Escaping ---
                # This ensures multi-line code from the LLM is written correctly to disk.
                if "content" in fc_args and isinstance(fc_args["content"], str):
                    try:
                        # Converts literal "\n" strings into actual newline characters
                        fc_args["content"] = fc_args["content"].encode().decode('unicode_escape')
                    except Exception as e:
                        if args.verbose:
                            print(f"Warning: Could not decode content escape characters: {e}")
                # ----------------------------------------

                if "working_directory" not in fc_args:
                    fc_args["working_directory"] = "."

                g_function_call = types.FunctionCall(
                    name=tool_call.function.name, 
                    args=fc_args, 
                    call_id=tool_call.id
                )

                function_call_result = call_function(g_function_call, verbose=args.verbose)
                
                if function_call_result.parts:
                    resp_part = function_call_result.parts[0]
                    function_responses.append(types.Part(
                        function_response={
                            "id": tool_call.id, 
                            "response": resp_part.function_response
                        }
                    ))
                
                if args.verbose:
                    print(f"-> Executed Tool: {tool_call.function.name}")

            messages.append(types.Content(role="user", parts=function_responses))
        
        else:
            if message.content:
                print(f"\nFinal response:\n{message.content}")
            else:
                print("\nFinal response: [No content returned]")
            return

    print("Error: Maximum iterations (20) reached.")
    sys.exit(1)

if __name__ == "__main__":
    main()