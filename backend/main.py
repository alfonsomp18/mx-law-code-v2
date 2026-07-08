import os
import time
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

GITHUB_USER = os.getenv("GITHUB_USER", "alfonsomp18")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_TIMEOUT = 10
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "60"))
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000"
).split(",")

app = FastAPI(title="GitHub Repos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["Accept"],
)

_cache: dict = {"data": None, "at": 0.0}


@app.get("/api/repos")
async def get_repos():
    if _cache["data"] and time.monotonic() - _cache["at"] < CACHE_TTL:
        return _cache["data"]

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

    result = [
        {
            "name": r["name"],
            "description": r["description"],
            "url": r["html_url"],
            "language": r["language"],
            "stars": r["stargazers_count"],
            "updated_at": r["updated_at"],
        }
        for r in resp.json()
    ]

    _cache["data"] = result
    _cache["at"] = time.monotonic()
    return result


@app.get("/health")
async def health():
    return {"status": "ok"}


# Serve frontend — must be mounted last so API routes take precedence
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
