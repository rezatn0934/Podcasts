from fastapi import Request, HTTPException
from config.config import settings
import httpx


class DjangoClient:
    channels_list_url = settings.CHANNEL_LIST_URL
    podcast_url = settings.PODCAST_URL

    async def _send_request(self, url: str, request: Request):
        headers = {'correlation-id': request.state.correlation_id}
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

    async def get_channels(self, request: Request):
        return await self._send_request(self.channels_list_url, request)

    async def get_channels_items(self, request: Request, channel_id: int):
        url = f"{self.channels_list_url}{channel_id}/"
        return await self._send_request(url, request)

    async def get_single_item(self, request: Request, podcast_id: int):
        url = f"{self.podcast_url}{podcast_id}/"
        return await self._send_request(url, request)


def get_django_client():
    return DjangoClient()