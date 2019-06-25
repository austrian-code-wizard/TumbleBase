from dataclasses import dataclass
from datetime import datetime
from model.enums import MessageType


@dataclass
class BaseClass:

    # primary key
    id: int = None

    # override to_string method
    def __str__(self):
        model_as_string = self.__class__.__name__ + ": "
        first_line = True
        for field_name in self.__dataclass_fields__.keys():
            column_value = str(getattr(self, field_name))
            if first_line:
                model_as_string += field_name + "=" + column_value
                first_line = False
            else:
                model_as_string += ", " + field_name + "=" + column_value
        model_as_string += ";"
        return model_as_string

    @classmethod
    def create_from_dao(cls, dao):
        dto = cls()
        for column_name in dao.__table__.columns.keys():
            setattr(dto, column_name, getattr(dao, column_name))
        return dto

    @classmethod
    def create_from_dao_list(cls, dao_list):
        dto_list = list()
        for dao in dao_list:
            dto_list.append(cls.create_from_dao(dao))
        return dto_list


@dataclass
class Packet(BaseClass):
    # primary key and foreign keys
    id: int = None

    # table attributes
    packet_number: int = None
    timestamp: datetime = None
    content: str = None

    # relationships
    message_id: int = None


@dataclass
class Message(BaseClass):

    # attributes
    message: str = None
    saved_at: datetime = None

    # primary key and foreign keys
    id: int = None

    # table attributes
    message_number: int = None
    address: str = None
    time_begin_sending: datetime = None
    time_done_sending: datetime = None
    type: str = None
    value: str = None
    done: bool = None
    message_type: MessageType = None

    # relationships
    packets: Packet = None # TODO: not sure if this is how it works

