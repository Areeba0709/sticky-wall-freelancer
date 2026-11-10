import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

# Timeout in milliseconds (120 seconds)
client = genai.Client(api_key=GEMINI_API_KEY, http_options={'timeout': 120000})

MODELS_TO_TRY = ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite']

def _call_gemini(prompt):
    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json" if "JSON" in prompt else "text/plain")
            )
            return response.text
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue
    return None

def parse_brain_dump(text):
    prompt = f"""
    You are an expert productivity assistant. I will give you a messy "brain dump" of thoughts.
    Extract the tasks from this text and return a JSON list. 
    Each item in the list must have these exact keys:
    - "title": (string) A short, clear title of the task.
    - "category": (string) Must be exactly one of: "Work", "Personal", or "Urgent".
    - "amount": (number) If a dollar amount is mentioned (e.g., $50), put the number here. Otherwise, 0.

    Here is the brain dump:
    "{text}"
    """
    result = _call_gemini(prompt)
    if result:
        try:
            return json.loads(result)
        except:
            return []
    return []

def generate_daily_report(completed_tasks):
    if not completed_tasks:
        return "No tasks completed today yet. Get to work! 🥐"
        
    tasks_text = "\n".join(completed_tasks)
    prompt = f"""
    You are a professional AI assistant. Here is a list of tasks I completed today:
    {tasks_text}
    
    Write a short, encouraging, and professional paragraph summarizing my day. 
    Include a fun bakery pun at the end.
    """
    result = _call_gemini(prompt)
    return result if result else "AI failed to generate report."