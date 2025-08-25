import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS

def main():
    load_dotenv()
    if len(sys.argv) == 1:
        print('No prompt provided. Use format [main.py "Your_prompt_here"]')
        sys.exit(1)
    
    if sys.argv[-1] == "--verbose":
        verbose = True
        user_prompt = " ".join(sys.argv[1:-1])
    else:
        verbose = False
        user_prompt = " ".join(sys.argv[1:])
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_ITERS:
            print("Max iterations reached, exiting.")
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    if not response.function_calls:
        return response.text
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("Empty function response")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("No function responses generated, exiting.")
    
    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()