import enum
from datetime import datetime, timedelta

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VideoStatus(str, enum.Enum):
    NEW = "new"
    TRANSCODED = "transcoded"
    RECOGNIZED = "recognized"


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_path: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration: Mapped[timedelta] = mapped_column(INTERVAL, nullable=False)
    camera_number: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[VideoStatus] = mapped_column(
        SAEnum(
            VideoStatus,
            name="video_status",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        default=VideoStatus.NEW,
        server_default=VideoStatus.NEW.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
