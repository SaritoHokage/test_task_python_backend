from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.video import VideoStatus


class VideoCreate(BaseModel):
    video_path: str = Field(min_length=1)
    start_time: datetime
    duration: timedelta
    camera_number: int = Field(gt=0)
    location: str = Field(min_length=1)

    @field_validator("duration")
    @classmethod
    def duration_must_be_positive(cls, v: timedelta) -> timedelta:
        if v.total_seconds() <= 0:
            raise ValueError("duration must be positive")
        return v


class VideoStatusUpdate(BaseModel):
    status: VideoStatus


class VideoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    video_path: str
    start_time: datetime
    duration: timedelta
    camera_number: int
    location: str
    status: VideoStatus
    created_at: datetime
