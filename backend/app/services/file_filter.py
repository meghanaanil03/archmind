IMPORTANT_FILENAMES = {
    "package.json",
    "requirements.txt",
    "readme.md",
    "main.py",
    "app.py",
    "index.js",
    "app.jsx",
    "app.tsx",
    "vite.config.js",
    "vite.config.ts",
}


def filter_files(files: list[dict]) -> list[dict]:
    scored = []

    for file in files:
        score = 0
        path = file["path"].lower()
        name = path.split("/")[-1]

        if name in IMPORTANT_FILENAMES:
            score += 5

        if "src/" in path or "app/" in path or "server/" in path or "backend/" in path:
            score += 2

        if "test" in path:
            score -= 1

        if len(file["content"].strip()) > 50:
            score += 1

        item = file.copy()
        item["score"] = score
        scored.append(item)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored