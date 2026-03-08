from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".md", ".json", ".html", ".css"
}

IGNORED_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    ".next",
    "__pycache__",
    "venv",
    ".venv",
    ".idea",
    ".vscode",
}

IGNORED_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
}


def build_preview(content: str, max_lines: int = 40, max_chars: int = 1500) -> str:
    lines = content.splitlines()
    preview = "\n".join(lines[:max_lines])
    return preview[:max_chars]


def load_repository(repo_path: str) -> list[dict]:
    root = Path(repo_path)

    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid repo path: {repo_path}")

    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        if path.name in IGNORED_FILES:
            continue

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                content = path.read_text(encoding="latin-1")
            except Exception:
                continue
        except Exception:
            continue

        normalized_path = str(path.relative_to(root)).replace("\\", "/")
        lines = content.splitlines()

        files.append({
            "path": normalized_path,
            "name": path.name,
            "extension": path.suffix.lower(),
            "content": content[:12000],   # keep for later deeper analysis
            "preview": build_preview(content),
            "line_count": len(lines),
            "char_count": len(content),
        })

    return files