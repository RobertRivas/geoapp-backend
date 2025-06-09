from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import asyncio
from typing import AsyncGenerator
import config  # Import the config module

# database url

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL


class Database:
    # constructor
    def __init__(self, database_url: str):
        # async engine creation
        self.engine = create_async_engine(database_url)
        # initialize base class for auto mapping postgres database schema.
        self.Base = automap_base()
        # async session created
        self.async_session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def prepare_base(self):
        async with self.engine.begin() as conn:
            # reflects database schema
            await conn.run_sync(lambda conn: self.Base.prepare(autoload_with=conn))
            # makes table accessible through sqlalchemy repeat process for more tables as needed.
            self.NYCNeighborhood = self.Base.classes.nyc_neighborhoods
            self.NYCHomicides = self.Base.classes.nyc_homicides

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


# Initialize the Database instance
database = Database(SQLALCHEMY_DATABASE_URL)
