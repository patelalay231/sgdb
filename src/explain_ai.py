import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import explain_ai
load_dotenv()

def explain(signal, line, code):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    response = ""
    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""The program crashed due to the following signal: SIGSEGV.
This error occurred in the function main at line 42 . Here is the relevant code snippet that caused the issue: int *ptr = NULL; *ptr = 1; return explanation of error in simple term and must return explaination in max 2-3 lines."""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""The program crashed because you tried to write a value (1) to a memory location that your program doesn't have permission to access. You created a pointer named 'ptr' and set it to 'NULL', which means it doesn't point to any valid memory. Then, you tried to use the '*' operator to write the value 1 to the address that 'ptr' holds (which is nothing, because it's NULL). This is like trying to put something into a box that doesn't exist.  This is a common error called a segmentation fault (SIGSEGV) and it usually means you're trying to access memory you shouldn't.\n"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=generate_prompt(signal,line,code)),
            ],
        ),
    ]
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
    ):
        if(chunk.text is not None):
            response += chunk.text
    return response
    
def generate_prompt(signal, line, code):
    prompt = f"""The program crashed due to the following signal: {signal}.This error occurred at line {line}. Here is the relevant code snippet that caused the issue: {code}."""
    return prompt

if __name__ == "__main__":
    # comment while testing
    signal, line, code = sys.argv[1:]
    print("\n=== Program Information ===")
    print(code)
    print("\nRunning AI explanation...\n")
    print(explain(signal, line, code))

