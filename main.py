import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
    """
    Call Gemini with function calling support.
    """
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        # model="gemini-1.5-flash-002",
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, temperature=0, tools=[available_functions]
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:")
    if response.function_calls:
        function_results = []

        for function_call in response.function_calls:
            # 1. Ejecutar la función
            function_call_result = call_function(function_call, verbose=args.verbose)

            # 2. Validaciones de seguridad de la estructura
            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts")

            part = function_call_result.parts[0]
            if not part.function_response:
                raise RuntimeError("Part does not contain a function_response")

            if part.function_response.response is None:
                raise RuntimeError("FunctionResponse.response is None")

            # 3. Guardar el resultado
            function_results.append(part)

            # 4. Feedback visual si es verbose
            if args.verbose:
                print(f"-> {part.function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
