from pathlib import Path
from openai import OpenAI # type: ignore
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "reviewer_prompt.txt"


def build_reviewer_context(files: list[dict]) -> str:
    chunks = []

    for f in files:
        chunks.append(
            f"FILE: {f['path']}\n"
            f"EXTENSION: {f['extension']}\n"
            f"LINES: {f.get('line_count', 0)}\n"
            f"CONTENT:\n{f['content'][:3500]}"
        )

    return "\n\n".join(chunks)


def run_reviewer_agent(selected_files: list[dict]):

    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
    context = build_reviewer_context(selected_files)

    user_input = f"""
Files for Review:

{context}
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