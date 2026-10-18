# Descriptive Statistics API

FastAPI service for `GET /stats?values=1,2,3` with strict CORS for `https://dash-zfmw2q.example.com`.

## Deploy on Render

1. Create a GitHub repository and upload `main.py`, `requirements.txt`, and `render.yaml` from this folder.
2. In Render, choose **New + → Blueprint** and connect that GitHub repository.
3. Deploy the service. Render will provide a public HTTPS URL; that is the base URL to submit.

## Local run

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Test:

```bash
curl "http://127.0.0.1:8000/stats?values=1,2,3,4"
curl -i -X OPTIONS "http://127.0.0.1:8000/stats" -H "Origin: https://dash-zfmw2q.example.com" -H "Access-Control-Request-Method: GET"
curl -i -X OPTIONS "http://127.0.0.1:8000/stats" -H "Origin: https://evil.example" -H "Access-Control-Request-Method: GET"
```

The allowed preflight should return 204 with the exact `Access-Control-Allow-Origin`; the disallowed preflight should return 403 without that header. Every response includes `X-Request-ID` and `X-Process-Time`.
