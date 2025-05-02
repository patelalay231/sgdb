import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()

# Initialize client ONCE
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)


system_instruction = open('utils/system_instruction.txt', "r").read()

# Conversation memory
contents = []

def generate_response():
    model = "gemini-2.0-flash-lite"
    response = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        config=types.GenerateContentConfig(
            temperature=0.5,
            system_instruction = system_instruction,
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["root_cause_found", "follow_up_required"],
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
                "fix_suggestion": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "follow_up_command": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
        ),
        contents=contents,
    ):
        if chunk.text is not None:
            response += chunk.text
    return response


while True:
    input_text = input("You: ")
    
    if input_text.lower() == "exit":
        print("Exiting the chat. Goodbye!")
        break

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=input_text)],
        ),
    )

    response = generate_response()
    parsed_response = json.loads(response)

    print("AI: ", parsed_response)
    contents.append(
        role="model",
        parts=[types.Part.from_text(text=response)],
    )
