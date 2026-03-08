def build_tree_text(files: list[dict]) -> str:
    return "\n".join(file["path"] for file in files)