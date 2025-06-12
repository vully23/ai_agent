import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    if len(sys.argv) == 1:
        print("No prompt given")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
    args = []
    for arg in sys.argv:
        if not arg.startswith("--"):
            args.append(arg)
    prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    print(response.text)
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()