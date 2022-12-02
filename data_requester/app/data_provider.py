"""
Module provide a class that is responsible
for getting the response from the server
"""

import logging

import aiohttp
from prometheus_client import Counter

# Global variables from prometheus metrics:
REQUEST_CNT = Counter("request", "Sent request count")
SUCCESS_RESPONSE_CNT = Counter("success_response", "Received response with valid data")
ERROR_RESPONSE_CNT = Counter("error_response", "Received response with error count")

logger = logging.getLogger(__name__)


class DataProvider:
    """
    Class that is connecting to our server and
    returns response from the server if available

    Variables:
    - base_url: URL must be provided to find our server

    Methods:
    - get_pairs(): returns the currency pairs if available
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def __send_request(self, path: str, params: dict) -> dict:
        """Function that returns a response from http server"""
        logger.debug("Send HTTP request")
        logger.debug(f"Full path: {path}, additional params: {params}")

        async with aiohttp.ClientSession() as session:
            async with session.get(path, params=params) as response:
                if response.status == 200:
                    logger.debug(
                        f"Successfully get data with status: {response.status}"
                    )
                    SUCCESS_RESPONSE_CNT.inc()
                    return await response.json()
                    
                ERROR_RESPONSE_CNT.inc()
                logger.error(f"Status of the response: {response.status}")
                logger.error(await response.text())
                return {}

    async def get_pairs(self) -> dict:
        """Function that returns currency pairs from response"""
        logger.debug("Getting correct currency pairs")
        response = await self.__send_request(path=self.base_url, params={})
        return response
