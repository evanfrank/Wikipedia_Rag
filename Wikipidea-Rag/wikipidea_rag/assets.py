from dagster import (  # AssetExecutionContext,
                     MetadataValue,
                     asset,
                     MaterializeResult)

from .asset_functions import (parse_dump_page,
                              parse_dump_section)

from .resources import postgres_con
import pandas as pd
import requests
import os
import zipfile


@asset
def download_data() -> MaterializeResult:
    "https://dumps.wikimedia.org/enwiki/"
    url = "https://dumps.wikimedia.org/enwiki/"
    html = requests.get(url).content
    df_list = pd.read_html(html)

    return MaterializeResult(
        metadata={
            "length of docks": len(list),
            "files in data": file,
            "preview": MetadataValue.md(df_list.head().to_markdown())
        }
    )


@asset
def unzip_data() -> MaterializeResult:
    file = fr"{os.getcwd()}\wikipidea_rag\data\{list[1]})"

    with zipfile.ZipFile("file.zip", "r") as zip_ref:
        zip_ref.extractall(r"wikipidea_rag\data")

    return MaterializeResult(
        metadata={
            "length of docks": len(list),
            "files in data": file,
        }
    )


@asset(deps=[unzip_data])
def stream_page_to_db(localDB: postgres_con) -> MaterializeResult:
    list = os.listdir(r'wikipidea_rag\data')

    print(list.sort())

    file = fr"{os.getcwd()}\wikipidea_rag\data\{list[1]})"

    parse_dump_page(file, localDB.make_con())
    return MaterializeResult(
        metadata={
            "length of docks": len(list),
            "files in data": file,
            # "preview": MetadataValue.md(bouy_meta.head().to_markdown())
        }
    )


@asset(deps=[unzip_data])
def stream_section_to_db(localDB: postgres_con) -> MaterializeResult:
    list = os.listdir(r'wikipidea_rag\data')

    print(list.sort())

    file = fr"{os.getcwd()}\wikipidea_rag\data\{list[1]})"

    parse_dump_section(file, localDB.make_con())
    return MaterializeResult(
        metadata={
            "length of docks": len(list),
            "files in data": file,
            # "preview": MetadataValue.md(bouy_meta.head().to_markdown())
        }
    )
