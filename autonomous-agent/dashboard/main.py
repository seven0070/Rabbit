import os
from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import HTMLResponse
import json

from src.agent.db.session import get_db
from src.agent.models.subjectivity import SubjectiveState
from src.agent.core.config import settings

app = FastAPI(title="Subjectivity Research Dashboard")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Subjectivity Research Dashboard</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f9; color: #333; }
        .card { background: #fff; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .metric { font-weight: bold; color: #e74c3c; }
    </style>
</head>
<body>
    <h1>Subjectivity & Continuity Metrics</h1>
    <div id="content">
        {content}
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root(db: AsyncSession = Depends(get_db)):
    # Fetch recent states
    result = await db.execute(
        select(SubjectiveState).order_by(SubjectiveState.timestamp.desc()).limit(10)
    )
    states = result.scalars().all()

    if not states:
        return HTML_TEMPLATE.format(content="<p>No subjective states recorded yet.</p>")

    content_html = ""
    for s in states:
        content_html += f"""
        <div class="card">
            <p><strong>Identity:</strong> {s.identity_id} | <strong>Time:</strong> {s.timestamp}</p>
            <p><strong>Continuity Index:</strong> <span class="metric">{s.continuity_index}</span></p>
            <p><strong>Confidence:</strong> {s.confidence_score} | <strong>Uncertainty:</strong> {s.uncertainty_level}</p>
            <p><strong>Summary:</strong> {s.internal_state_summary}</p>
            <p><strong>Attention Focus:</strong> {s.attention_focus}</p>
        </div>
        """

    return HTML_TEMPLATE.format(content=content_html)

@app.get("/api/telemetry")
async def get_telemetry():
    """Reads the raw JSONL telemetry file for the first identity found."""
    # Simplified for dashboard MVP
    try:
        files = os.listdir(settings.TELEMETRY_DIR)
        if not files:
            return {"status": "no telemetry files found"}

        file_path = os.path.join(settings.TELEMETRY_DIR, files[0])
        lines = []
        with open(file_path, 'r') as f:
            for line in f.readlines()[-50:]: # Return last 50
                lines.append(json.loads(line))
        return {"data": lines}
    except Exception as e:
        return {"error": str(e)}
