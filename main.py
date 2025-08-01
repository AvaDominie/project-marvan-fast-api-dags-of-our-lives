from fastapi import FastAPI
import snowflake.connector
import logging 
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

logger = logging.getLogger("data_staging")
logger.setLevel(logging.INFO)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}





# access the CA gold data through an endpoint ID
@app.get("/CA-Gold-Data/{ID}")
async def read_data(ID: int):
    # Snowflake credentials
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
    SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA_GOLD = os.getenv('SNOWFLAKE_SCHEMA_GOLD')
    SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
    SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA_GOLD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        role=SNOWFLAKE_ROLE
    )
    sf_cursor = conn.cursor()
    sf_cursor.execute(f"SELECT * FROM CA_TESTS_VS_ANTIBODIES WHERE ID = {ID}")
    data = sf_cursor.fetchone()
    logger.info("Connected to Snowflake successfully.")

    # Format data for endpoint


    # Close connection
    conn.close()

    # Return data
    return { "data": data }  # Return data in a dictionary format







@app.get("/CA-Covid-Data/{ID}")
async def read_data(ID: int):

    # Snowflake credentials
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
    SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA_SILVER = os.getenv('SNOWFLAKE_SCHEMA_SILVER')
    SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
    SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')


    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA_SILVER,
        warehouse=SNOWFLAKE_WAREHOUSE,
        role=SNOWFLAKE_ROLE
    )
    sf_cursor = conn.cursor()
    sf_cursor.execute(f"SELECT * FROM SILVER_CA_ANTIBODY WHERE ID = {ID}")
    data = sf_cursor.fetchone()
    logger.info("Connected to Snowflake successfully.")


    # Format data for endpoint




    # Close connection
    conn.close()

    # Return data
    return { "data": data }  # Return data in a dictionary format
