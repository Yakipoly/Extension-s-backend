from peewee import (
    fn,
    Model,
    PrimaryKeyField,
    IntegerField,
    TextField,
    DoubleField,
    CharField,
    DateField,
    TimeField,
    PostgresqlDatabase,
    OperationalError,
    SmallIntegerField,
)
from os import environ

database = PostgresqlDatabase(
    environ["POSTGRES_DB"],
    user=environ["POSTGRES_USER"],
    password=environ["POSTGRES_PASSWORD"],
    host=environ["POSTGRES_HOST"],
    autorollback=True,
)


def create_connection():
    try:
        database.connection()
    except OperationalError:
        database.connect(reuse_if_open=True)


def destroy_connection():
    database.close()


class DatabaseConnection:
    def __enter__(self):
        try:
            database.connection()
        except OperationalError:
            database.connect(reuse_if_open=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        database.close()


class BaseModel(Model):
    class Meta:
        database = database


class DESC_SALE(BaseModel):
    id = PrimaryKeyField(null=False)
    description = TextField()
    md5_hash = TextField()

    class Meta:
        table_name = "desc_list"


class DESC_RENT(BaseModel):
    id = PrimaryKeyField(null=False)
    description = TextField()
    md5_hash = TextField()

    class Meta:
        table_name = "rent_desc_list"


class Search(BaseModel):
    id = PrimaryKeyField(null=False)
    index_id = IntegerField(null=True)
    original_id = IntegerField(null=True)

    id_address_adverts = IntegerField()
    price = IntegerField(null=True)
    id_description = IntegerField(null=True)

    date = DateField()

    id_site = IntegerField(null=True)
    id_category = IntegerField(null=True)

    rooms = IntegerField()
    object_type = IntegerField()
    building_type = IntegerField()
    level = IntegerField()
    levels = IntegerField()
    wall = IntegerField()
    is_deleted = IntegerField(null=True)

    area = DoubleField()
    area_kitchen = DoubleField()
    area_living = DoubleField()
    area_room = DoubleField()
    area_house = DoubleField()
    area_land = DoubleField()
    area_total = DoubleField()

    lat = DoubleField()
    lon = DoubleField()

    fias_id2 = IntegerField()
    fias_street2 = IntegerField()
    fias_city2 = IntegerField()
    fias_area2 = IntegerField()
    fias_city_district2 = IntegerField()
    fias_settlement2 = IntegerField()

    postal_code = IntegerField(null=True)

    class Meta:
        table_name = "searching_sale"


class SEARCH_SALE(Search):
    class Meta:
        table_name = "searching_sale"


class SEARCH_RENT(Search):
    class Meta:
        table_name = "searching_rent"
