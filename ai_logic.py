from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an expert resume reviewer and career coach.
You will receive:
- A resume (text)
- A job description (text)

Your task:
1. Score how well the resume matches the job description from 0 to 100.
2. List important missing keywords/skills from the job description.
3. Suggest 3 to 5 tailored bullet points the user could add or adapt in their resume.

Respond ONLY with valid JSON in this exact structure:
{
  "match_score": 0,
  "missing_keywords": ["keyword1", "keyword2"],
  "tailored_bullets": ["bullet1", "bullet2", "bullet3"]
}
Do not add any extra text before or after the JSON.
"""

DUMMY_RESULT = {
    "match_score": 70,
    "missing_keywords": ["example_skill", "example_tool"],
    "tailored_bullets": [
        "Added a bullet demonstrating relevant skill for the role.",
        "Highlighted a project that matches key job requirements.",
        "Quantified impact with numbers (e.g., improved X by Y%)."
    ]
}

def analyze_resume(resume_text: str, jd_text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
                }
            ],
            temperature=0.3,
        )

        content = response.choices.message.content.strip()
        # In case the model adds some extra text, try to extract JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end > start:
            content = content[start:end]

        return json.loads(content)

    except RateLimitError as e:
        # No credits / rate limit
        print("RateLimitError (no credits). Using dummy result.")
        print("Error:", e)
        return DUMMY_RESULT

    except Exception as e:
        # Any other error
        print("General error. Using dummy result.")
        print("Error:", e)
        return DUMMY_RESULT