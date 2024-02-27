# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, Depends, Security, Form, Body, Query
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN
from os import environ
from pydantic import BaseModel, Field
from typing import Optional, List
from models import DatabaseConnection, DESC_RENT, DESC_SALE, SEARCH_SALE, SEARCH_RENT
import hashlib
from re import sub
from setproctitle import setproctitle

setproctitle(f"API_RASHIR")

app = FastAPI(
    docs_url=f"/{environ['API_URL']}/documentation",
    redoc_url=f"/{environ['API_URL']}/redocumentation",
    root_path="/",
    openapi_url=f"/{environ['API_URL']}/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_key_header = APIKeyHeader(name="token", auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    """
    Функция для получения API ключа.

    Parameters:
    api_key_header (str): Заголовок API ключа.

    Returns:
    str: Возвращает API ключ, если он совпадает с переменными среды "TOKEN" или "TOKEN_PUBLIC".

    Raises:
    HTTPException: Если ключ не прошел валидацию, возникает исключение с кодом 403 (HTTP_403_FORBIDDEN) и детальным сообщением "Could not validate credentials".
    """
    if api_key_header == environ["TOKEN"] or api_key_header == environ["TOKEN_PUBLIC"]:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


###############################################################################################################
class Item(BaseModel):
    type_table: str = Field(
        default="sale",
        enum=["sale", "rent"],
        title="тип базы",
        description="аренда или продажа",
    )
    description: str = Field(default="", title="Описание")


class HashOpisOut200(BaseModel):
    status: str = "success"
    type_table: str
    data: List[int]
    count: int
    id_description: int


class HashOpisOut400(BaseModel):
    detail: str


@app.post(
    "/chrome_ext/hash_opis",
    responses={200: {"model": HashOpisOut200}, 400: {"model": HashOpisOut400}},
)
async def hash_opis(item: Item):
    
    """
    Функция для хеширования описания товара и поиска его в базе данных.

    Parameters:
    item (Item): Объект товара, содержащий описание для хеширования.

    Returns:
    dict: Возвращает словарь с информацией о статусе операции, типе таблицы товаров, данными, количеством результатов и идентификатором описания товара.

    Raises:
    HTTPException: В случае, если длина описания товара равна нулю, вызывается исключение с кодом 400 (Bad Request) и детальным сообщением "Hash len zero".
    """
    
    if len(item.description) == 0:
        raise HTTPException(status_code=400, detail="Hash len zero")
    T = DESC_SALE if item.type_table == "sale" else DESC_RENT
    S = SEARCH_SALE if item.type_table == "sale" else SEARCH_RENT
    md5_hash = hashlib.md5(
        str.upper(sub(r"[^A-Za-zА-Яа-яёЁ0-9]", "", item.description)).encode("utf-8")
    ).hexdigest()
    with DatabaseConnection():
        try:
            ID_DESCRIPTION = (
                T.select(T.id).where(T.md5_hash == md5_hash).limit(1).scalar()
            )
        except:
            return {
                "status": "success",
                "type_table": item.type_table,
                "data": [],
                "count": 0,
                "id_description": 0,
            }
        if not ID_DESCRIPTION:
            return {
                "status": "success",
                "type_table": item.type_table,
                "data": [],
                "count": 0,
                "id_description": 0,
            }

        answer = [
            item.index_id
            for item in S.select(S.index_id).where(
                (S.is_deleted.is_null(True)) & (S.id_description == ID_DESCRIPTION)
            )
        ]
        answer.sort(reverse=True)
        return {
            "status": "success",
            "type_table": item.type_table,
            "data": answer,
            "count": len(answer),
            "id_description": ID_DESCRIPTION,
        }
