import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts import ANALYSIS_PROMPT, RESPONSE_PROMPT

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"

def load_knowledge_base():
    with open("knowledge_base.json", "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_job(user_input: str) -> dict:
    kb = load_knowledge_base()
    prompt = ANALYSIS_PROMPT.format(
        knowledge_base=json.dumps(kb),
        user_input=user_input
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0,
        top_p=1.0,
        seed=42
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input: str, analysis: dict, action: str) -> str:
    prompt = RESPONSE_PROMPT.format(
        action=action,
        analysis=json.dumps(analysis),
        user_input=user_input
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        top_p=1.0,
        seed=42
    )
    return response.choices[0].message.content