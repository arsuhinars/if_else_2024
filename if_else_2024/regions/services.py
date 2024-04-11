from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.repositories import AccountRepository
from if_else_2024.core.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    IntegrityBreachException,
)
from if_else_2024.regions.dto import (
    CreateRegionDto,
    CreateRegionTypeDto,
    UpdateRegionDto,
    UpdateRegionTypeDto,
)
from if_else_2024.regions.models import Region, RegionType
from if_else_2024.regions.repositories import RegionRepository, RegionTypeRepository


class RegionTypeService:
    def __init__(
        self, repository: RegionTypeRepository, region_repository: RegionRepository
    ):
        self._repository = repository
        self._region_repository = region_repository

    async def create(self, session: AsyncSession, dto: CreateRegionTypeDto):
        if await self._repository.exists_by_type(session, dto.type):
            raise EntityAlreadyExistsException(
                "RegionType with given type already exists"
            )

        region_type = RegionType(**dto.model_dump())

        return await self._repository.save(session, region_type)

    async def get_by_id(self, session: AsyncSession, id: int):
        region_type = await self._repository.get_by_id(session, id)
        if region_type is None:
            raise EntityNotFoundException("RegionType with given id was not found")
        return region_type

    async def update_by_id(
        self, session: AsyncSession, id: int, dto: UpdateRegionTypeDto
    ):
        region_type = await self._repository.get_by_id(session, id)
        if region_type is None:
            raise EntityNotFoundException("RegionType with given id was not found")

        if dto.type != region_type.type and await self._repository.exists_by_type(
            session, dto.type
        ):
            raise EntityAlreadyExistsException(
                "RegionType with given type already exists"
            )

        region_type.type = dto.type

        return await self._repository.save(session, region_type)

    async def delete_by_id(self, session: AsyncSession, id: int):
        region_type = await self._repository.get_by_id(session, id)
        if region_type is None:
            raise EntityNotFoundException("RegionType with given id was not found")

        if await self._region_repository.exists_by_type_id(session, id):
            raise IntegrityBreachException(
                "There are some regions with given RegionType"
            )

        await self._repository.delete(session, region_type)


class RegionService:
    def __init__(
        self,
        repository: RegionRepository,
        region_type_repository: RegionTypeRepository,
        account_repository: AccountRepository,
    ):
        self._repository = repository
        self._region_type_repository = region_type_repository
        self._account_repository = account_repository

    async def create(
        self, session: AsyncSession, account_id: int, dto: CreateRegionDto
    ):
        if await self._repository.exists_by_location(
            session, dto.latitude, dto.longitude
        ):
            raise EntityAlreadyExistsException(
                "Region with given latitude and longitude already exists"
            )

        if await self._repository.exists_by_name(session, dto.name):
            raise EntityAlreadyExistsException("Region with given name already exists")

        region_type = await self._region_type_repository.get_by_id(
            session, dto.region_type_id
        )
        if region_type is None:
            raise EntityNotFoundException("RegionType with given id was not found")

        parent_region = None
        if dto.parent_region_name is not None:
            parent_region = await self._repository.get_by_name(
                session, dto.parent_region_name
            )
            if parent_region is None:
                raise EntityNotFoundException(
                    "Parent Region with given name was not found"
                )

        account = await self._account_repository.get_by_id(session, account_id)
        if account is None:
            raise EntityNotFoundException("Account with given id was not found")

        region = Region(
            **dto.model_dump(exclude=["parent_region_name", "region_type_id"]),
            region_type=region_type,
            account=account,
            parent_region=parent_region
        )

        return await self._repository.save(session, region)

    async def get_by_id(self, session: AsyncSession, id: int):
        region = await self._repository.get_by_id(session, id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")
        await region.awaitable_attrs.parent_region
        return region

    async def update_by_id(
        self, session: AsyncSession, id: int, account_id: int, dto: UpdateRegionDto
    ):
        region = await self._repository.get_by_id(session, id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        if dto.name != region.name and await self._repository.exists_by_name(
            session, dto.name
        ):
            raise EntityAlreadyExistsException("Region with given name already exists")

        if (
            dto.latitude != region.latitude
            and dto.longitude != region.longitude
            and await self._repository.exists_by_location(
                session, dto.latitude, dto.longitude
            )
        ):
            raise EntityAlreadyExistsException(
                "Region with latitude and longitude name already exists"
            )

        parent_region = await region.awaitable_attrs.parent_region
        parent_region_name = None if parent_region is None else parent_region.name
        if dto.parent_region_name != parent_region_name:
            if dto.parent_region_name is None:
                region.parent_region = None
            else:
                parent_region = await self._repository.get_by_name(
                    session, dto.parent_region_name
                )
                if parent_region is None:
                    raise EntityNotFoundException(
                        "Parent Region with given name was not found"
                    )
                if parent_region.id == id:
                    raise IntegrityBreachException("Region can not be parent of itself")
                region.parent_region = parent_region

        if dto.region_type_id != region.region_type_id:
            region_type = await self._region_type_repository.get_by_id(
                session, dto.region_type_id
            )
            if region_type is None:
                raise EntityNotFoundException("RegionType with given id was not found")
            region.region_type = region_type

        if account_id != region.account_id:
            account = self._account_repository.get_by_id(session, account_id)
            if account is None:
                raise EntityNotFoundException("Account with given id was not found")
            region.account = account

        region.name = dto.name
        region.latitude = dto.latitude
        region.longitude = dto.longitude

        return await self._repository.save(session, region)

    async def delete_by_id(self, session: AsyncSession, id: int):
        region = await self._repository.get_by_id(session, id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        if await self._repository.exists_by_parent_id(session, id):
            raise IntegrityBreachException("Region is parent of some regions")

        await self._repository.delete(session, region)
