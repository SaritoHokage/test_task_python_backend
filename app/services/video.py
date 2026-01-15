from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import Video, VideoStatus
from app.repositories.video import VideoRepository
from app.schemas.video import VideoCreate, VideoRead, VideoStatusUpdate


class VideoService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = VideoRepository(session)

    async def create(self, payload: VideoCreate) -> VideoRead:
        video = Video(
            video_path=payload.video_path,
            start_time=payload.start_time,
            duration=payload.duration,
            camera_number=payload.camera_number,
            location=payload.location,
            status=VideoStatus.NEW,
        )
        created = await self._repo.add(video)
        return VideoRead.model_validate(created)

    async def get(self, video_id: int) -> VideoRead:
        video = await self._repo.get(video_id)
        if video is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
        return VideoRead.model_validate(video)

    async def list(
        self,
        *,
        statuses: list[VideoStatus] | None,
        camera_numbers: list[int] | None,
        locations: list[str] | None,
        start_time_from: datetime | None,
        start_time_to: datetime | None,
    ) -> list[VideoRead]:
        videos = await self._repo.list(
            statuses=statuses,
            camera_numbers=camera_numbers,
            locations=locations,
            start_time_from=start_time_from,
            start_time_to=start_time_to,
        )
        return [VideoRead.model_validate(v) for v in videos]

    async def update_status(self, video_id: int, payload: VideoStatusUpdate) -> VideoRead:
        video = await self._repo.get(video_id)
        if video is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
        updated = await self._repo.update_status(video, payload.status)
        return VideoRead.model_validate(updated)
