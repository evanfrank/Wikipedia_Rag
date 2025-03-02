import pandas as pd
import os

from dagster import (  # AssetExecutionContext,
                     MetadataValue,
                     asset,
                     MaterializeResult)

from .resources import postgres_con

from .asset_functions import parse_dump


@asset
def stream_date_to_db(localDB: postgres_con) -> MaterializeResult:
    list = os.listdir('wikipidea_rag\data')
    print(list)

    parse_dump()
    return MaterializeResult(
        metadata={
            "length of docks": len(list),
        }
    )


@asset
def bouy_names(localDB: postgres_con) -> MaterializeResult:
    engine = localDB.make_con()

    bouy_meta = pd.read_xml("https://www.ndbc.noaa.gov/activestations.xml")

    sql = 'SELECT table_name FROM information_schema.tables \
           WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\';'
    tables = pd.read_sql(sql, con=engine)

    if tables.isin(["BouyMeta"]).any().any():
        sql = "SELECT * FROM public.\"BouyMeta\";"
        bouy_loaded = pd.read_sql(sql, con=engine)
        existing_bouys = bouy_loaded['id'].values
        bouy_meta = bouy_meta[~bouy_meta['id'].isin(existing_bouys)]

        bouy_meta.to_sql("BouyMeta",
                         con=engine,
                         if_exists='append',
                         index=False)
    else:
        bouy_meta.to_sql("BouyMeta",
                         con=engine,
                         if_exists='append',
                         index=False)

    return MaterializeResult(
        metadata={
            "num_records": len(bouy_meta),
            "preview": MetadataValue.md(bouy_meta.head().to_markdown()),
        }
    )
