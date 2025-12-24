import os
from utils.get_env import get_app_data_directory_env, get_database_url_env
from urllib.parse import urlsplit, urlunsplit, parse_qsl
import ssl
from sqlalchemy import Engine

def get_database_url_and_connect_args(database_url: str) -> tuple[str, dict]:
    if not database_url.startswith('sqlite://'):
        raise ValueError("database_url must start with sqlite://")

    connect_args = {"check_same_thread": False}

    try:
        split_result = urlsplit(database_url)
        if split_result.query:
            query_params = parse_qsl(split_result.query, keep_blank_values=True)
            driver_scheme = split_result.scheme
            for k, v in query_params:
                key_lower = k.lower()
                if key_lower == "sslmode" and "postgresql+asyncpg" in driver_scheme:
                    if v.lower() != "disable" and "sqlite" not in database_url:
                        connect_args["ssl"] = ssl.create_default_context()

            database_url = urlunsplit(
                (
                    split_result.scheme,
                    split_result.netloc,
                    split_result.path,
                    "",
                    split_result.fragment,
                )
            )
    except Exception as e:
        pass

    return database_url, connect_args

def get_existing_tables_in_db(engine: Engine)->list:
    return engine.table_names()