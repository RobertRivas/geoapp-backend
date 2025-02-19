from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import database
from geoalchemy2.functions import ST_AsGeoJSON
import json
app = FastAPI()


async def get_db():
    await database.prepare_base()
    async with database.async_session_maker() as session:
        yield session


@app.get("/")
async def root():
    return {"message": "Hello World"}


# defines endpoint
@app.get("/neighborhoods")
# defines function to grab list of neighborhoods in nyc_neighborhoods table
# depends on get_db to provide AsyncSession instance.
async def nyc_neighborhoods(db: AsyncSession = Depends(get_db)):

    # executes query to postGIS "SELECT * FROM nyc_neighborhoods"
    result = await db.execute(select(database.NYCNeighborhood))
    # selects all rows from nyc_neighborhoods
    neighborhoods = result.scalars().all()
    features = []
    for neighborhood in neighborhoods:
        # geometry conversion to GeoJSON
        geometry = await db.scalar(ST_AsGeoJSON(neighborhood.geom))
        # creates feature dictionary
        feature = {
            "type": "Feature",
            "geometry": json.loads(geometry),
            "properties": {
                "name": neighborhood.name
                # Add other properties as needed
            }
        }
        features.append(feature)
# creates feature collection from the appended features above in GeoJSON format
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson
