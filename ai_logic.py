from openai import OpenAI, RateLimitError
import os
import json

def get_openai_client():
    import streamlit as st
    key = None
    if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
        key = st.secrets["OPENAI_API_KEY"]
    else:
        key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=key)

client = get_openai_client()

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

def analyze_resume(resume_text, job_description_text, use_dummy=True):
    if use_dummy:
        return DUMMY_RESULT

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description_text}"}
            ],
            temperature=0.3,
            max_tokens=500
        )
        result_text = response.choices[0].message.content.strip()
        return json.loads(result_text)
    except RateLimitError:
        return {
            "match_score": -1,
            "missing_keywords": ["API rate limit reached"],
            "tailored_bullets": ["Please try again in a few minutes."]
        }
    except Exception as e:
        return {
            "match_score": -1,
            "missing_keywords": ["Error during analysis"],
            "tailored_bullets": [f"Error: {str(e)}"]
        }
