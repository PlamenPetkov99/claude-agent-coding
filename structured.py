import json
import anthropic
import sys
import re


client = anthropic.Anthropic()

job_text = """
Junior Machine Learning Engineer at HFT Architecture. Fully remote, from anywhere
in the world. USD 125,000-155,000 per year. You'll write Python daily including
tests, and should be able to explain why ordinary cross-validation breaks on time
series. A personal project to show is required.
"""

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": f"Extract title, company, remote, salary_min, salary_max and "
                   f"required_skills from this job post. Return JSON.\n\n{job_text}",
    }],
)

text = next(block.text for block in response.content if block.type == "text")
print("RAW TEXT:\n", text)

match = re.search(r"```json\s*(.*?)```", text, flags=re.DOTALL)
if match:
    text = match.group(1).strip()  # JSON string

data = json.loads(text)
print("PARSED:\n", data)