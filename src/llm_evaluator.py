from groq import Groq
import json
import os
from src.utils import clean_resume_text
from config import GROQ_API_KEY

# Load API key from environment variable or config
api_key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY
client = Groq(api_key=api_key)

def evaluate_resume(jd, resume_text):

    resume_text = clean_resume_text(resume_text)

    prompt = f"""
You are a strict technical recruiter.

Evaluate the candidate ONLY based on the given Job Description.

JOB DESCRIPTION:
{jd}

RESUME:
{resume_text}

SCORING RULES:
- Strong match: 8-10
- Partial match: 5-7
- Weak match: 0-4
- Prefer real projects over theory
- Penalize vague resumes

OUTPUT STRICTLY IN JSON:
{{
  "score": number,
  "category": "Shortlist | Maybe | Reject",
  "strengths": ["point1", "point2"],
  "weaknesses": ["point1", "point2"],
  "reasoning": "brief explanation"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Use available model
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        
        # Strip markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        if content.endswith("```"):
            content = content[:-3]  # Remove ```
        content = content.strip()
        
        # Try to parse JSON
        result = json.loads(content)
        
        # Validate required fields
        required_fields = ["score", "category", "strengths", "weaknesses", "reasoning"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
        
        return result

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw content: {content}")
        return {
            "score": 0,
            "category": "Reject",
            "strengths": [],
            "weaknesses": ["Invalid response format"],
            "reasoning": f"LLM returned invalid JSON: {e}"
        }
    except Exception as e:
        print("Groq error:", e)
        return {
            "score": 0,
            "category": "Reject",
            "strengths": [],
            "weaknesses": ["LLM failed"],
            "reasoning": f"Evaluation failed: {e}"
        }