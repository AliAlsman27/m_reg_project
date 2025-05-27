from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    _id: Optional[ObjectId]
    project_name: str = Field(..., min_length=1)
    project_id: str




    @validator('project_id')
    def validate_project_id(cls, v):
        if not value.isalnum():
            raise ValueError('Project ID must be a alphanumeric string')
        return v

        class Config:
            arbitrary_types_allowed = True

            