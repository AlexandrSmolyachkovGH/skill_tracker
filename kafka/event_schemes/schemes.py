from datetime import datetime
from enum import Enum
from uuid import uuid4

from django.utils import timezone
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=timezone.now)


class AnalyticsEventType(str, Enum):
    PROJECT_CREATED = "project_created"
    PROJECT_MEMBER_ADDED = "project_member_added"
    TASK_CREATED = "task_created"
    TASK_STATUS_CHANGED = "task_status_changed"
    TASK_COMPLETED = "task_completed"


class AnalyticsEvent(BaseEvent):
    event_type: AnalyticsEventType
    project_id: str
    user_id: str
    task_id: str | None = None
    metadata: dict | None = None
