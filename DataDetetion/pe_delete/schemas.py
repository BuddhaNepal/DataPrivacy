from typing import List, Optional

from pydantic import BaseModel
from datetime import date

from pe_delete import models


class EDiscovery(BaseModel):
    legal_hold: bool = False

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    address: str
    birthdate: date
    blood_group: str
    company: str
    job: str
    name: str
    sex: str
    ssn: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# NEW


class DeletionAPIBase(BaseModel):
    name: str
    description: Optional[str] = None
    api_type: models.APIType
    api_field: models.APIFieldType
    url: str


class DeletionAPICreate(DeletionAPIBase):
    pass


class DeletionAPI(DeletionAPIBase):
    id: int
    deletion_service_id: int

    class Config:
        orm_mode = True


class DeletionServiceBase(BaseModel):
    name: str
    description: str


class DeletionServiceCreate(DeletionServiceBase):
    pass


class DeletionService(DeletionServiceBase):
    id: int
    apis: List[DeletionAPI] = []

    class Config:
        orm_mode = True
