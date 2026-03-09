from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from app.services.repo_loader import load_repository
from app.services.file_filter import filter_files
from app.services.tree_builder import build_tree_text
from app.agents.architect_agent import run_architect_agent
from app.agents.reviewer_agent import run_reviewer_agent

app = FastAPI(title="ArchMind API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        architect_result = run_architect_agent(tree, filtered_files)
        selected_files_paths = architect_result["selected_files"]

        selected_files = [
            f for f in filtered_files
            if f["path"] in selected_files_paths
        ]

        reviewer_summary = run_reviewer_agent(selected_files)

        return {
            "repo_path": request.repo_path,
            "file_count": len(filtered_files),
            "tree": tree,
            "architect_scout": architect_result["scout_result"],
            "selected_files": architect_result["selected_files"],
            "architect_summary": architect_result["final_summary"],
            "reviewer_summary": reviewer_summary
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")