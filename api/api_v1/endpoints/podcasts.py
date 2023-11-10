from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer

from schemas.interaction import InteractionSchema, BaseInteractionSchema
from services.api_services import get_api_service
from services.authentication import get_access_jwt_aut

api_router = APIRouter()


@api_router.get("/channels")
async def channels_list(request: Request, api_service=Depends(get_api_service)):
    response = await api_service.channels_list(request=request)
    return response


@api_router.get("/channels/{channel_id}")
async def channels_items(channel_id: int, request: Request, api_service=Depends(get_api_service),
                         payload: HTTPBearer = Depends(get_access_jwt_aut())):
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required for this API")

    response = await api_service.get_channels_items(request=request, channel_id=channel_id, user_id=user_id)
    return response


@api_router.get('/podcasts/{podcast_id}')
async def single_item(podcast_id: int, request: Request, api_service=Depends(get_api_service),
                      payload: HTTPBearer = Depends(get_access_jwt_aut())):
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required for this API")
    response = await api_service.get_single_item(request=request, podcast_id=podcast_id, user_id=user_id)
    return response


@api_router.post('/interaction')
async def interaction_with_item(interaction: InteractionSchema,
                                api_service=Depends(get_api_service),
                                payload: HTTPBearer = Depends(get_access_jwt_aut())):
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required for this API")
    response = await api_service.interaction_with_item(user_id=user_id, interaction=interaction)
    return response


@api_router.post('/remove_interaction')
async def remove_interaction(interaction: BaseInteractionSchema, api_service=Depends(get_api_service),
                             payload: HTTPBearer = Depends(get_access_jwt_aut())):
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required for this API")
    response = await api_service.remove_interaction(user_id=user_id, interaction=interaction)
    return response
