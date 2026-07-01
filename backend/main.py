import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GitHub Repos API")

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1,null"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["Accept"],
)

GITHUB_USER = os.getenv("GITHUB_USER", "alfonsomp18")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")  # optional — avoids rate limits
GITHUB_API_TIMEOUT = 10  # seconds


@app.get("/api/repos")
async def get_repos():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        async with httpx.AsyncClient(timeout=GITHUB_API_TIMEOUT) as client:
            resp = await client.get(
                f"https://api.github.com/users/{GITHUB_USER}/repos",
                params={"per_page": 100, "sort": "updated"},
                headers=headers,
            )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="GitHub API timed out")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="GitHub API error")

    repos = resp.json()
    return [
        {
            "name": r["name"],
            "description": r["description"],
            "url": r["html_url"],
            "language": r["language"],
            "stars": r["stargazers_count"],
            "updated_at": r["updated_at"],
        }
        for r in repos
    ]


@app.get("/health")
async def health():
    return {"status": "ok"}
