from __future__ import annotations

import ipaddress
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from support_toolkit import build_report

logger = logging.getLogger(__name__)
APP_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="IT Support Toolkit",
    description="Coleta somente leitura para diagnóstico local de estações.",
    version="2.2.0",
)

# Reject unexpected Host headers (including most DNS-rebinding attempts).
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "[::1]"],
)


@app.middleware("http")
async def require_loopback_client(request: Request, call_next):
    """The dashboard has no login; never serve it to a remote network client."""
    client_host = request.client.host if request.client else ""
    try:
        client_address = ipaddress.ip_address(client_host)
    except ValueError:
        client_address = None

    if client_address is None or not client_address.is_loopback:
        return JSONResponse(
            status_code=403,
            content={
                "detail": (
                    "Acesso remoto bloqueado. Execute o dashboard localmente "
                    "em 127.0.0.1."
                )
            },
        )

    return await call_next(request)


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
