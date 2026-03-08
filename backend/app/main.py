from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.repo_loader import load_repository
from app.services.file_filter import filter_files
from app.services.tree_builder import build_tree_text
from app.agents.architect_agent import run_architect_agent

app = FastAPI(title="ArchMind API")


class LocalRepoRequest(BaseModel):
    repo_path: str


@app.get("/")
def root():
    return {"message": "ArchMind backend is running"}


@app.post("/analyze/local")
def analyze_local_repo(request: LocalRepoRequest):
    try:
        
        files = load_repository(request.repo_path)
        filtered_files = filter_files(files)
        tree = build_tree_text(filtered_files)
        architect_summary = run_architect_agent(tree, filtered_files)

        return {
            "repo_path": request.repo_path,
            "file_count": len(filtered_files),
            "tree": tree,
            "architect_summary": architect_summary
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")