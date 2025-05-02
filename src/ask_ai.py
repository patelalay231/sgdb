import base64
from google.genai import types
from google import genai
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()

system_instruction = open('utils/system_instruction.txt', "r").read()

def generate_response(history,system_instruction):
    model = "gemini-2.0-flash-lite"
    response = ""
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        config=types.GenerateContentConfig(
            temperature=0.5,
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
        contents=history,
    ):
        if chunk.text is not None:
            response += chunk.text
    return response

if __name__ == "__main__":
    history = sys.argv[1]
    system_instruction = sys.argv[2]
    response = generate_response(history, system_instruction)

    parsed_response = json.loads(response)
    print(parsed_response)