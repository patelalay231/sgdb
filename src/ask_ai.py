import base64
from google.genai import types
from google import genai
from dotenv import load_dotenv
import os
import sys
import json
import inspect

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
HISTORY_PATH = os.path.join(BASE_DIR,"history.txt")
UTILS_PATH = os.path.join(BASE_DIR, "utils")
SYSTEM_INSTRUCTION_PATH = os.path.join(UTILS_PATH, "system_instruction.txt")

with open(SYSTEM_INSTRUCTION_PATH, "r") as f:
    system_instruction = f.read()

with open(HISTORY_PATH, "r") as f:
    history = f.read()

def generate_response():
    model = "gemini-2.0-flash"
    response = ""
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        config=types.GenerateContentConfig(
            temperature=0.8,
            system_instruction = system_instruction,
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["root_cause_found", "follow_up_required","root_cause_analysis", "follow_up_command"],
            properties = {
                "root_cause_found": genai.types.Schema(
                    type = genai.types.Type.BOOLEAN,
                ),
                "follow_up_required": genai.types.Schema(
                    type = genai.types.Type.BOOLEAN,
                ),
                "root_cause_analysis": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "follow_up_command": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "code_fix_suggestion": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
        ),
        contents=f"Past conversations :- {history}",
    ):
        if chunk.text is not None:
            response += chunk.text
    return response

if __name__ == "__main__":
    response = generate_response()

    parsed_response = json.loads(response)
    print(parsed_response)