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

        files.append({
            "path": str(path.relative_to(root)).replace("\\", "/"),
            "extension": path.suffix.lower(),
            "content": content[:12000],
        })

    return files