from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.models import Account
from if_else_2024.auth.utils import pass_context
from if_else_2024.forecasts.models import Forecast
from if_else_2024.regions.models import Region, RegionType
from if_else_2024.weather.models import Weather, WeatherCondition


class FakeDataCreator:
    def __init__(
        self,
        accounts_count: int,
        region_types_count: int,
        regions_count: int,
        forecasts_count: int,
        weather_count: int,
    ):
        self.__accounts_count = accounts_count
        self.__region_types_count = region_types_count
        self.__regions_count = regions_count
        self.__forecasts_count = forecasts_count
        self.__weather_count = weather_count
        self.__faker = Faker(locale="ru_RU", use_weighting=False)

    async def create(self, session: AsyncSession):
        q = select(Account).limit(self.__accounts_count)
        accounts = list((await session.execute(q)).scalars().all())

        q = select(RegionType).limit(self.__region_types_count)
        region_types = list((await session.execute(q)).scalars().all())

        q = select(Region).limit(self.__regions_count)
        regions = list((await session.execute(q)).scalars().all())

        q = select(Forecast).limit(self.__forecasts_count)
        forecasts = list((await session.execute(q)).scalars().all())

        q = select(Weather).limit(self.__weather_count)
        weather = list((await session.execute(q)).scalars().all())

        for i in range(self.__accounts_count - len(accounts)):
            accounts.append(
                Account(
                    first_name=self.__faker.first_name(),
                    last_name=self.__faker.last_name(),
                    email=self.__faker.email(),
                    password_hash=pass_context.hash(self.__faker.password()),
                )
            )

        for i in range(self.__region_types_count - len(region_types)):
            region_types.append(
                RegionType(
                    type=self.__faker.country(),
                )
            )
        session.add_all(accounts)
        session.add_all(region_types)
        await session.flush()

        for i in range(self.__regions_count - len(regions)):
            regions.append(
                Region(
                    region_type_id=self.__faker.random_element(region_types).id,
                    account_id=self.__faker.random_element(accounts).id,
                    name=self.__faker.city(),
                    parent_region_id=(
                        self.__faker.random_element(regions).id
                        if (self.__faker.pybool() and len(regions) > 0)
                        else None
                    ),
                    latitude=float(self.__faker.latitude()),
                    longitude=float(self.__faker.longitude()),
                    current_weather_id=None,
                )
            )
        session.add_all(regions)
        await session.flush()

        for i in range(self.__forecasts_count - len(forecasts)):
            forecasts.append(
                Forecast(
                    date_time=self.__faker.date_time_this_month(after_now=True),
                    temperature=self.__faker.pyfloat(min_value=-30.0, max_value=30.0),
                    weather_condition=self.__faker.enum(WeatherCondition),
                    region_id=self.__faker.random_element(regions).id,
                )
            )

        for i in range(self.__weather_count - len(weather)):
            weather.append(
                Weather(
                    region_id=self.__faker.random_element(regions).id,
                    temperature=self.__faker.pyfloat(min_value=-30.0, max_value=30.0),
                    humidity=self.__faker.pyfloat(min_value=0.0, max_value=100.0),
                    wind_speed=self.__faker.pyfloat(min_value=0.0, max_value=100.0),
                    weather_condition=self.__faker.enum(WeatherCondition),
                    precipitation_amount=self.__faker.pyfloat(
                        min_value=0.0, max_value=100.0
                    ),
                    measurement_date_time=self.__faker.date_time_this_decade(
                        before_now=True
                    ),
                )
            )

        session.add_all(forecasts)
        session.add_all(weather)
        await session.flush()
        await session.commit()

    async def release(self, session: AsyncSession):
        # for account in self.__accounts:
        #     await session.delete(account)
        # await session.flush()
        # await session.commit()
        pass
