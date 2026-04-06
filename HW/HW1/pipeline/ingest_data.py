#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click
from tqdm.auto import tqdm


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table_name', default='yellow_taxi_data', help='Target table name')
def run(user, password, host, port, db, table_name):
    # Ingestion logic here 

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("Reading parquet file...")
    df_green = pd.read_parquet('green_tripdata_2025-11.parquet')
    print(f"Reading complete, total rows: {len(df_green)}")

    print(f"Creating table {table_name}...")
    df_green.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    # insert data in chunks to avoid memory issues
    print("Importing data...")
    chunksize = 10000
    for i in range(0, len(df_green), chunksize):
        chunk = df_green.iloc[i:i+chunksize]
        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False
        )
        print(f"Imported {i+len(chunk)}/{len(df_green)} rows")
    
    print(f"Data import completed! Total rows: {len(df_green)}")


    df_zones = pd.read_csv('taxi_zone_lookup.csv')
    df_zones.to_sql(
        name='zones',
        con=engine,
        if_exists="replace"
    )
    print("Zones table created")

if __name__ == '__main__':
    run()



