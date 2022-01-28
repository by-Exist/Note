from __future__ import annotations

import typing
from pydantic import BaseModel, Extra, UUID4, Field
from uuid import uuid4


class _BaseDomainModel(BaseModel):
    class Config:
        # Class
        orm_mode = True  # Model.from_orm 활성화
        # Initialization
        extra = Extra.ignore  # 필드로 정의되지 않은 키워드 인자 무시
        allow_population_by_field_name = True  # Field alias로 전달된 키워드 인자 허용

    def __eq__(self, other: typing.Any):
        return type(self) is type(other) and self.__dict__ == other.__dict__


class ValueObject(_BaseDomainModel):
    class Config(_BaseDomainModel.Config):
        frozen = True  # 필드 값 변경 불가, __hash__ 메서드 제공


if typing.TYPE_CHECKING:
    PropertySchema = dict[str, typing.Any]
    PropertiesSchema = dict[str, PropertySchema]
    ModelSchema = dict[str, typing.Any | PropertiesSchema]


class Entity(_BaseDomainModel):

    id: UUID4 = Field(default_factory=uuid4, allow_mutation=False)

    class Config(_BaseDomainModel.Config):
        # Class
        validate_assignment = True  # 속성 할당 시 유효성 검사 수행

    def __eq__(self, other: typing.Any):
        if type(self) is type(other):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):  # type: ignore
        return hash(self.id)


class Aggregate(Entity):

    version: int = Field(default=0)

    class Config(Entity.Config):
        ...
