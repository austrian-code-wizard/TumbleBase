from sqlalchemy import Column, ForeignKey, Table, Integer, String, Enum, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func

Base = declarative_base()


class BaseWithConverter(Base):
    __abstract__ = True

    # override to_string method
    def __str__(self):
        model_as_string = self.__tablename__ + ": "
        first_line = True
        for column_name in self.__table__.columns.keys():
            column_value = str(getattr(self, column_name))
            if first_line:
                model_as_string += column_name + "=" + column_value
                first_line = False
            else:
                model_as_string += ", " + column_name + "=" + column_value
        model_as_string += ";"
        return model_as_string

    @classmethod
    def create_from_dto(cls, dto):
        dao = cls()
        for key in dto.__dataclass_fields__.keys():
            setattr(dao, key, getattr(dto, key))
        return dao

    @classmethod
    def create_from_dto_list(cls, dto_list):
        dao_list = list()
        for dto in dto_list:
            dao_list.append(cls.create_from_dto(dto))
        return dao_list


class Image(BaseWithConverter):
    __tablename__ = "image"

    # primary key and foreign keys
    id = Column(Integer, primary_key=True, autoincrement=True)

    # table attributes
    image_path = Column(String, nullable=False, unique=True)
    saved_at = Column(DateTime(timezone=True), nullable=False)

class Command(BaseWithConverter):
    __tablename__ = "command"

    # primary key and foreign keys
    id = Column(Integer, primary_key=True, autoincrement=True)

    # table attributes
    command = Column(String, nullable=False, unique=True)
    arguments = Column(String)
    saved_at = Column(DateTime(timezone=True), nullable=False)

class Message(BaseWithConverter):
    __tablename__ = "message"

    # primary key and foreign keys
    id = Column(Integer, primary_key=True, autoincrement=True)

    # table attributes
    message = Column(String, nullable=False)
    saved_at = Column(DateTime(timezone=True), nullable=False)
