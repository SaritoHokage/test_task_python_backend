from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.video import VideoStatus
from app.schemas.video import VideoCreate, VideoRead, VideoStatusUpdate
from app.services.video import VideoService

router = APIRouter(prefix="", tags=["videos"])


@router.post("/videos", response_model=VideoRead, status_code=status.HTTP_201_CREATED)
async def create_video(
    payload: VideoCreate,
    session: AsyncSession = Depends(get_session),
) -> VideoRead:
    return await VideoService(session).create(payload)


@router.get("/videos", response_model=list[VideoRead])
async def list_videos(
    status_: Annotated[list[VideoStatus] | None, Query(alias="status")] = None,
    camera_number: Annotated[list[int] | None, Query()] = None,
    location: Annotated[list[str] | None, Query()] = None,
    start_time_from: Annotated[datetime | None, Query()] = None,
    start_time_to: Annotated[datetime | None, Query()] = None,
    session: AsyncSession = Depends(get_session),
) -> list[VideoRead]:
    return await VideoService(session).list(
        statuses=status_,
        camera_numbers=camera_number,
        locations=location,
        start_time_from=start_time_from,
        start_time_to=start_time_to,
    )


@router.get("/videos/{video_id}", response_model=VideoRead)
async def get_video(
    video_id: int,
    session: AsyncSession = Depends(get_session),
) -> VideoRead:
    return await VideoService(session).get(video_id)


@router.patch("/videos/{video_id}/status", response_model=VideoRead)
async def update_video_status(
    video_id: int,
    payload: VideoStatusUpdate,
    session: AsyncSession = Depends(get_session),
) -> VideoRead:
    return await VideoService(session).update_status(video_id, payload)
