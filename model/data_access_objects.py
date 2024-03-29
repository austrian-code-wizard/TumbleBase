from sqlalchemy import Column, ForeignKey, Table, Integer, String, Enum, DateTime, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from model.enums import MessageType
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
            if not getattr(dto, key) is None:
                setattr(dao, key, getattr(dto, key))
        return dao

    @classmethod
    def create_from_dto_list(cls, dto_list):
        dao_list = list()
        for dto in dto_list:
            dao_list.append(cls.create_from_dto(dto))
        return dao_list


class Packet(BaseWithConverter):
    __tablename__ = "packet"

    # primary key and foreign keys
    id = Column(Integer, primary_key=True, autoincrement=True)

    # table attributes
    packet_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    content = Column(LargeBinary(length=256), nullable=False)

    # relationships
    message_id = Column(Integer, ForeignKey('message.id'))


class Message(BaseWithConverter):
    __tablename__ = "message"

    # primary key and foreign keys
    id = Column(Integer, primary_key=True, autoincrement=True)

    # table attributes
    message_number = Column(Integer, nullable=False)
    address = Column(String, nullable=True)
    time_begin_sending = Column(DateTime(timezone=True), nullable=False)
    time_done_sending = Column(DateTime(timezone=True))
    value_type = Column(String(length=2), nullable=False)
    total_packets = Column(Integer, nullable=False)
    data_type = Column(String(length=1), nullable=False)
    done = Column(Boolean, default=False)
    message_type = Column(Enum(MessageType), nullable=False)

    # relationships
    packets = relationship("Packet")
