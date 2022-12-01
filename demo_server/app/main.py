"""
Main function of our demo_server
"""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

import routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s",
)

logger = logging.getLogger("uvicorn.error")

# FastAPI application init:
app = FastAPI(
    title="Metrics Collector",
    description="Demo server that collects some metrics",
    version="0.0.1",
)

# Include our routes:
app.include_router(routes.router)
app.add_route("/metrics", handle_metrics)

# Adding Middleware
app.add_middleware(PrometheusMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    logger.info("Starting server")
    logger.warning("This is debug server")
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
