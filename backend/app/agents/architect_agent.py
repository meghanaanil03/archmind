import json
from pathlib import Path
from openai import OpenAI  # type: ignore
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent
SCOUT_PROMPT_PATH = BASE_DIR / "prompts" / "architect_scout_prompt.txt"
ARCHITECT_PROMPT_PATH = BASE_DIR / "prompts" / "architect_prompt.txt"


def build_compact_tree(files: list[dict], limit: int = 30) -> str:
    paths = [f["path"] for f in files[:limit]]
    return "\n".join(paths)


def build_file_summaries(files: list[dict], limit: int = 12) -> str:
    summaries = []

    for f in files[:limit]:
        summaries.append(
            f"FILE: {f['path']}\n"
            f"EXTENSION: {f['extension']}\n"
            f"LINES: {f.get('line_count', 0)}\n"
            f"CHARS: {f.get('char_count', 0)}\n"
            f"PREVIEW:\n{f.get('preview', '')}\n"
        )

    return "\n\n".join(summaries)


def fallback_select_files(files: list[dict], limit: int = 6) -> list[dict]:
    important_names = {
        "package.json",
        "requirements.txt",
        "readme.md",
        "main.py",
        "app.py",
        "index.js",
        "index.ts",
        "app.jsx",
        "app.tsx",
        "vite.config.js",
        "vite.config.ts",
        "tsconfig.json",
    }

    def score(file: dict) -> int:
        path = file["path"].lower()
        name = file["name"].lower()
        score = 0

        if name in important_names:
            score += 5
        if "server/" in path or "backend/" in path:
            score += 3
        if "src/" in path:
            score += 2
        if "db" in path or "config" in path or "auth" in path or "route" in path:
            score += 2
        if "test" in path:
            score -= 1

        return score

    ranked = sorted(files, key=score, reverse=True)
    return ranked[:limit]


def run_architect_scout(files: list[dict]) -> dict:
    prompt_text = SCOUT_PROMPT_PATH.read_text(encoding="utf-8")
    compact_tree = build_compact_tree(files)
    file_summaries = build_file_summaries(files)

    user_input = f"""
Repository Tree:
{compact_tree}

File Summaries:
{file_summaries}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content or "{}"

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "project_type": "Unknown",
            "architecture_guess": "Unknown",
            "important_files": []
        }


def select_files_from_scout(files: list[dict], scout_result: dict, limit: int = 6) -> list[dict]:
    requested_paths = {
        item.get("path", "").strip()
        for item in scout_result.get("important_files", [])
        if item.get("path")
    }

    selected = [f for f in files if f["path"] in requested_paths]

    if not selected:
        selected = fallback_select_files(files, limit=limit)

    return selected[:limit]


def build_deep_file_context(files: list[dict]) -> str:
    chunks = []

    for f in files:
        chunks.append(
            f"FILE: {f['path']}\n"
            f"EXTENSION: {f['extension']}\n"
            f"LINES: {f.get('line_count', 0)}\n"
            f"CONTENT:\n{f['content'][:3500]}"
        )

    return "\n\n".join(chunks)


def run_architect_agent(tree: str, files: list[dict]) -> dict:
    scout_result = run_architect_scout(files)
    selected_files = select_files_from_scout(files, scout_result)

    prompt_text = ARCHITECT_PROMPT_PATH.read_text(encoding="utf-8")
    compact_tree = build_compact_tree(files)
    deep_context = build_deep_file_context(selected_files)

    user_input = f"""
Repository Tree:
{compact_tree}

Scout Result:
Project Type Guess: {scout_result.get('project_type', 'Unknown')}
Architecture Guess: {scout_result.get('architecture_guess', 'Unknown')}

Selected Files For Deep Analysis:
{deep_context}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2,
    )

    final_summary = response.choices[0].message.content or "No summary returned."

    return {
        "scout_result": scout_result,
        "selected_files": [f["path"] for f in selected_files],
        "final_summary": final_summary
    }