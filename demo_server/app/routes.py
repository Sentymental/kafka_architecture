"""
Routes for our demo server
- get_pairs(): returns random currency value (dict)
"""

import random

import metrics
from fastapi import APIRouter
from prometheus_client import Counter

GET_PAIRS_COUNT = Counter("get_pairs", "Count of get pairs")

router = APIRouter()


@router.get("/pairs", tags=["pairs", "currency pairs"])
async def get_pairs() -> dict:
    """Function that generates currency randomly"""

    GET_PAIRS_COUNT.inc()
    return {
        "USDPLN": round(random.random() * 100, 2),
        "EURPLN": round(random.random() * 100, 2),
    }
