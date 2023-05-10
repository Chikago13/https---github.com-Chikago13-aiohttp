from sqlalchemy import Boolean, Column, Date, Identity, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Manufacturers(Base):
    __tablename__ = 'manufacturers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='manufacturers_pkey'),
        {'comment': 'Компании производители', 'schema': 'public'}
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone = Column(String)
    adress = Column(String)


class ManufacturersStorehouses(Base):
    __tablename__ = 'manufacturers_storehouses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='manufacturers_storehouses_pkey'),
        {'comment': 'Связь компании производителя и склада', 'schema': 'public'}
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    storehouses_id = Column(Integer, nullable=False)
    manufacturers_id = Column(Integer, nullable=False)


class ModelUser(Base):
    __tablename__ = 'model_user'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='model_user_pkey'),
        {'schema': 'public'}
    )

    id = Column(Integer)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    phone = Column(Text)


class Storehouses(Base):
    __tablename__ = 'storehouses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='storehouses_pkey'),
        {'comment': 'Склады', 'schema': 'public'}
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    adress = Column(String)


class Sweets(Base):
    __tablename__ = 'sweets'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sweets_pkey'),
        {'comment': 'Записи о сладостях', 'schema': 'public'}
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(String, nullable=False)
    cost = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    manufacturer_id = Column(Integer, nullable=False)
    production_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    sweets_types_id = Column(Integer)
    with_sugar = Column(Boolean)
    requires_freezing = Column(Boolean)


class SweetsTypes(Base):
    __tablename__ = 'sweets_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sweets_types_pkey'),
        {'comment': 'Виды сладостей', 'schema': 'public'}
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(String, nullable=False)


class UserToken(Base):
    __tablename__ = 'user_token'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_token_pkey'),
        {'schema': 'public'}
    )

    id = Column(Integer)
    user_id = Column(Integer, nullable=False)
    user_token = Column(Text, nullable=False)
    lvl = Column(Integer)
