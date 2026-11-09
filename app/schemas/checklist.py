from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import Timestamped


class ChecklistCreate(BaseModel):
    item_name: str = Field(min_length=1, max_length=250)
    is_completed: bool = False
    owner: str | None = None
    notes: str | None = None

    @field_validator("item_name", mode="before")
    @classmethod
    def trim_item_name(cls, value):
        return value.strip() if isinstance(value, str) else value


class ChecklistUpdate(BaseModel):
    item_name: str | None = Field(default=None, min_length=1, max_length=250)
    is_completed: bool | None = None
    owner: str | None = None
    notes: str | None = None

    @field_validator("item_name", mode="before")
    @classmethod
    def trim_item_name(cls, value):
        return value.strip() if isinstance(value, str) else value

    @model_validator(mode="after")
    def reject_null_item_name(self):
        if "item_name" in self.model_fields_set and self.item_name is None:
            raise ValueError("item_name cannot be null")
        if "is_completed" in self.model_fields_set and self.is_completed is None:
            raise ValueError("is_completed cannot be null")
        return self


class ChecklistRead(Timestamped):
    ai_system_id: int
    item_name: str
    is_completed: bool
    completed_at: datetime | None
    owner: str | None
    notes: str | None
