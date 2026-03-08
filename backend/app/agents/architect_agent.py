from pathlib import Path
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "architect_prompt.txt"


def run_architect_agent(tree: str, files: list[dict]):

    prompt_text = PROMPT_PATH.read_text()

    key_files = "\n\n".join(
        f"FILE: {f['path']}\n{f['content'][:3000]}"
        for f in files[:5]
    )

    user_input = f"""
Repository Tree:
{tree}

Key Files:
{key_files}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content