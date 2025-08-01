from fastapi import FastAPI
import snowflake.connector
import logging 
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

logger = logging.getLogger("data_staging")
logger.setLevel(logging.INFO)

def get_snowflake_connection(schema: str):
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=schema,
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        role=os.getenv('SNOWFLAKE_ROLE')
    )


# Filtering our gold table by ID
@app.get("/CA-Gold-Data/{ID}")
async def read_data(ID: int):
    conn = get_snowflake_connection(os.getenv('SNOWFLAKE_SCHEMA_GOLD'))
    sf_cursor = conn.cursor()
    sf_cursor.execute(f"SELECT * FROM CA_TESTS_VS_ANTIBODIES WHERE ID = {ID}")
    data = sf_cursor.fetchone()
    columns = [desc[0] for desc in sf_cursor.description]
    logger.info("Connected to Snowflake successfully.")
    formatted_data = dict(zip(columns, data)) if data else None
    conn.close()
    return {"formatted_data": formatted_data}


#  Filtering by location (province)
@app.get("/CA-Gold-Data-By-Province/{geo}")
async def read_data_by_province(geo: str):
    conn = get_snowflake_connection(os.getenv('SNOWFLAKE_SCHEMA_GOLD'))
    sf_cursor = conn.cursor()
    sf_cursor.execute(f"SELECT * FROM CA_TESTS_VS_ANTIBODIES WHERE GEO = '{geo}'")
    data = sf_cursor.fetchall()
    columns = [desc[0] for desc in sf_cursor.description]
    logger.info("Connected to Snowflake successfully.")
    formatted_data = [dict(zip(columns, row)) for row in data] if data else None
    conn.close()
    return {"formatted_data": formatted_data}




#  We're filtring these out based on the working age group

# get all ANTIBODIES_BOTH_SEXES_AGES_20_TO_59
@app.get("/CA-Gold-Data-Antibodies-Both-Sexes-Ages-20-To-59-and-geo")
async def read_antibodies_data():
    conn = get_snowflake_connection(os.getenv('SNOWFLAKE_SCHEMA_GOLD'))
    sf_cursor = conn.cursor()
    sf_cursor.execute("SELECT ANTIBODIES_BOTH_SEXES_AGES_20_TO_59, GEO FROM CA_TESTS_VS_ANTIBODIES")
    data = sf_cursor.fetchall()
    columns = [desc[0] for desc in sf_cursor.description]
    logger.info("Connected to Snowflake successfully.")
    formatted_data = [dict(zip(columns, row)) for row in data] if data else None
    conn.close()
    return {"formatted_data": formatted_data}

