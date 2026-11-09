from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import Timestamped


class AISystemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    owner: str = Field(min_length=1, max_length=200)
    department: str = Field(min_length=1, max_length=200)
    business_purpose: str = Field(min_length=1)
    technology_stack: str | None = None
    deployment_status: str = Field(default="planned", min_length=1, max_length=50)

    @field_validator("name", "owner", "department", "business_purpose", "deployment_status", mode="before")
    @classmethod
    def trim_required_strings(cls, value):
        return value.strip() if isinstance(value, str) else value


class AISystemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    owner: str | None = Field(default=None, min_length=1, max_length=200)
    department: str | None = Field(default=None, min_length=1, max_length=200)
    business_purpose: str | None = Field(default=None, min_length=1)
    technology_stack: str | None = None
    deployment_status: str | None = Field(default=None, min_length=1, max_length=50)

    @field_validator("name", "owner", "department", "business_purpose", "deployment_status", mode="before")
    @classmethod
    def trim_optional_strings(cls, value):
        return value.strip() if isinstance(value, str) else value

    @model_validator(mode="after")
    def reject_null_required_fields(self):
        required = {"name", "owner", "department", "business_purpose", "deployment_status"}
        for field in required & self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class AISystemRead(Timestamped):
    name: str
    description: str | None
    owner: str
    department: str
    business_purpose: str
    technology_stack: str | None
    deployment_status: str
