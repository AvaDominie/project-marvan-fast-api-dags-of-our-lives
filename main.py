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