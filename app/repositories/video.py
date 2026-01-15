from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import Video, VideoStatus


class VideoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, video: Video) -> Video:
        self._session.add(video)
        await self._session.commit()
        await self._session.refresh(video)
        return video

    async def get(self, video_id: int) -> Video | None:
        stmt = select(Video).where(Video.id == video_id)
        return await self._session.scalar(stmt)

    async def list(
        self,
        *,
        statuses: list[VideoStatus] | None = None,
        camera_numbers: list[int] | None = None,
        locations: list[str] | None = None,
        start_time_from: datetime | None = None,
        start_time_to: datetime | None = None,
    ) -> list[Video]:
        stmt = select(Video)

        if statuses:
            stmt = stmt.where(Video.status.in_(statuses))
        if camera_numbers:
            stmt = stmt.where(Video.camera_number.in_(camera_numbers))
        if locations:
            stmt = stmt.where(Video.location.in_(locations))
        if start_time_from:
            stmt = stmt.where(Video.start_time >= start_time_from)
        if start_time_to:
            stmt = stmt.where(Video.start_time <= start_time_to)

        stmt = stmt.order_by(Video.id.asc())
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def update_status(self, video: Video, new_status: VideoStatus) -> Video:
        video.status = new_status
        self._session.add(video)
        await self._session.commit()
        await self._session.refresh(video)
        return video
