from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from support_toolkit import build_report

logger = logging.getLogger(__name__)
APP_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="IT Support Toolkit",
    description="Coleta somente leitura para diagnóstico local de estações.",
    version="2.1.0",
)


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    try:
        html = (APP_DIR / "frontend.html").read_text(encoding="utf-8")
    except OSError as exc:
        logger.exception("Não foi possível carregar o dashboard.")
        raise HTTPException(
            status_code=500,
            detail="O dashboard não está disponível.",
        ) from exc
    return HTMLResponse(html)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}


@app.get("/diagnostic")
def diagnostic() -> dict:
    try:
        return build_report()
    except Exception as exc:
        logger.exception("A coleta de diagnóstico falhou.")
        raise HTTPException(
            status_code=500,
            detail="A coleta falhou. Consulte o log local para detalhes.",
        ) from exc
