import asyncio
import logging
from typing import Optional, List
import httpx

logger = logging.getLogger(__name__)

class ResilientRequestAdapter:
    """
    HTTP client adapter featuring exponential backoff retries and proxy pool rotation.
    """
    def __init__(self, proxies: Optional[List[str]] = None, max_retries: int = 3, backoff_factor: float = 0.5):
        self.proxies = proxies or []
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._proxy_index = 0

    def _get_next_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self._proxy_index % len(self.proxies)]
        self._proxy_index += 1
        return proxy

    async def get(self, url: str, headers: Optional[dict] = None) -> httpx.Response:
        last_error = None
        for attempt in range(self.max_retries):
            proxy = self._get_next_proxy()
            proxy_mount = {"all://": httpx.AsyncHTTPTransport(proxy=proxy)} if proxy else None
            
            try:
                async with httpx.AsyncClient(mounts=proxy_mount, timeout=10.0, headers=headers) as client:
                    response = await client.get(url)
                    if response.status_code in [429, 502, 503, 504]:
                        wait_time = self.backoff_factor * (2 ** attempt)
                        logger.warning(f"HTTP {response.status_code}. Retrying in {wait_time:.2f}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    response.raise_for_status()
                    return response
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_error = e
                wait_time = self.backoff_factor * (2 ** attempt)
                await asyncio.sleep(wait_time)
                
        raise RuntimeError(f"Request to {url} failed after {self.max_retries} retries. Last error: {last_error}")
