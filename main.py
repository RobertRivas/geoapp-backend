from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2 import functions as geo_func
import json
from geojson_pydantic import Feature, FeatureCollection
from database import database  # your db and models
import config  # Import the config module

frontend_origin = config.frontend_origin
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
async def get_db():
    await database.prepare_base()
    async with database.async_session_maker() as session:
        yield session


@app.get("/")
async def root():
    return {"message": "Hello World"}


# NYC Neighborhoods Endpoint
@app.get("/neighborhoods")
async def nyc_neighborhoods(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(database.NYCNeighborhood))
    neighborhoods = result.scalars().all()

    features = []
    for neighborhood in neighborhoods:
        # 💡 Transform to WGS84
        geometry_json = await db.scalar(
            geo_func.ST_AsGeoJSON(
                geo_func.ST_Transform(neighborhood.geom, 4326)
            )
        )
        geometry = json.loads(geometry_json)

        feature = Feature(
            type='Feature',
            geometry=geometry,
            properties={
                'gid': neighborhood.gid,
                'name': neighborhood.name,
                'borough': neighborhood.boroname,
            }
        )
        features.append(feature)

    return FeatureCollection(type='FeatureCollection', features=features)


# Homicides Endpoint
@app.get("/homicides")
async def nyc_homicides(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(database.NYCHomicides))
    homicides = result.scalars().all()

    features = []
    for homicide in homicides:
        # 💡 Transform to WGS84 for Supercluster compatibility
        geometry_json = await db.scalar(
            geo_func.ST_AsGeoJSON(
                geo_func.ST_Transform(homicide.geom, 4326)
            )
        )
        geometry = json.loads(geometry_json)

        feature = Feature(
            type='Feature',
            geometry=geometry,
            properties={
                'gid': homicide.gid,
                'incident_d': homicide.incident_d,
                'boroname': homicide.boroname,
                'num_victim': homicide.num_victim,
                'primary_mo': homicide.primary_mo,
                'id': homicide.id,
                'weapon': homicide.weapon,
                'light_dark': homicide.light_dark,
                'year': homicide.year
            }
        )
        features.append(feature)

    return FeatureCollection(type='FeatureCollection', features=features)
