# ArchMind

ArchMind is a multi-agent AI system that analyzes software repositories, identifies architecture, reviews code quality, and generates documentation.

## Overview

ArchMind is designed to act like an AI engineering team for a codebase. Instead of relying on a single prompt, it uses multiple specialized agents to inspect a repository and produce structured insights.

## Planned Features

- Repository ingestion from local paths and GitHub repositories
- Architect Agent for codebase structure and architecture analysis
- Reviewer Agent for code quality and maintainability feedback
- Documentation Agent for automated project summaries
- Multi-agent orchestration using LangGraph
- Dashboard for viewing analysis results

## Tech Stack

### Frontend
- React

### Backend
- FastAPI
- Python 3.11

### AI / Agent Framework
- OpenAI API
- LangGraph

### Repository Analysis
- GitPython
- File scanning and filtering

## Planned Agent Workflow

1. Load repository
2. Filter important files
3. Generate folder tree
4. Run Architect Agent
5. Run Reviewer Agent
6. Run Documentation Agent
7. Combine outputs into a final report

## Project Status

🚧 In progress

Current milestone:
- Initial repository setup
- Python 3.11 environment configured
- Core backend dependencies installed

## Future Improvements

- Dependency graph visualization
- Security analysis agent
- Semantic code search
- GitHub repository URL ingestion
- Exportable architecture reports