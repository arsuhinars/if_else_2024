from typing import Annotated

from annotated_types import Ge
from pydantic import AliasPath, BaseModel, ConfigDict, Field

from if_else_2024.utils import NonEmptyStr


class RegionTypeDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str


class CreateRegionTypeDto(BaseModel):
    type: Annotated[str, NonEmptyStr]


class UpdateRegionTypeDto(BaseModel):
    type: Annotated[str, NonEmptyStr]


class RegionDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    region_type_id: Annotated[
        int, Field(serialization_alias="regionType", validation_alias="region_type_id")
    ]
    account_id: Annotated[int, Field(serialization_alias="accountId")]
    name: str
    parent_region_name: Annotated[
        str | None,
        Field(
            serialization_alias="parentRegion",
            validation_alias=AliasPath("parent_region", "name"),
        ),
    ] = None
    latitude: float
    longitude: float


class CreateRegionDto(BaseModel):
    name: Annotated[str, NonEmptyStr]
    parent_region_name: Annotated[str | None, Field(alias="parentRegion"), NonEmptyStr]
    region_type_id: Annotated[int, Field(alias="regionType"), Ge(1)]
    latitude: float
    longitude: float


class UpdateRegionDto(BaseModel):
    name: Annotated[str, NonEmptyStr]
    parent_region_name: Annotated[str | None, Field(alias="parentRegion"), NonEmptyStr]
    region_type_id: Annotated[int, Field(alias="regionType"), Ge(1)]
    latitude: float
    longitude: float
