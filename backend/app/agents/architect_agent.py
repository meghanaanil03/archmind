from pathlib import Path
from openai import OpenAI  # type: ignore
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "architect_prompt.txt"


def is_architecture_relevant(file: dict) -> bool:
    path = file["path"].lower()
    name = file["name"].lower()

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

    if name in important_names:
        return True

    keywords = [
        "src/",
        "server/",
        "backend/",
        "routes",
        "route",
        "api",
        "db",
        "config",
        "main",
        "app",
        "index",
        "auth",
    ]

    return any(keyword in path for keyword in keywords)


def select_architect_files(files: list[dict], limit: int = 8) -> list[dict]:
    selected = [f for f in files if is_architecture_relevant(f)]

    def score(file: dict) -> int:
        path = file["path"].lower()
        name = file["name"].lower()
        score = 0

        if name in {"package.json", "requirements.txt", "readme.md"}:
            score += 5
        if name in {"main.py", "app.py", "index.js", "index.ts", "app.jsx", "app.tsx"}:
            score += 5
        if "server/" in path or "backend/" in path:
            score += 3
        if "src/" in path:
            score += 2
        if "db" in path or "config" in path or "auth" in path or "route" in path:
            score += 2

        return score

    selected.sort(key=score, reverse=True)
    return selected[:limit]


def build_compact_tree(files: list[dict], limit: int = 30) -> str:
    paths = [f["path"] for f in files[:limit]]
    return "\n".join(paths)


def run_architect_agent(tree: str, files: list[dict]):
    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")

    selected_files = select_architect_files(files)
    compact_tree = build_compact_tree(files)

    key_files = "\n\n".join(
        (
            f"FILE: {f['path']}\n"
            f"EXTENSION: {f['extension']}\n"
            f"LINES: {f['line_count']}\n"
            f"CHARS: {f['char_count']}\n"
            f"PREVIEW:\n{f['preview']}"
        )
        for f in selected_files
    )

    user_input = f"""
Repository Tree:
{compact_tree}

Key File Summaries:
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