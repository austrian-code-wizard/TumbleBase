from model.data_transfer_objects import Packet, Message
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from model.enums import MessageType
from datetime import datetime
from util.fields import BytesField


class PacketSchema(Schema):
    # primary key and foreign keys
    id = fields.Int(dump_only=True)

    # table attributes
    packet_number = fields.Int(allow_none=False, required=True)
    timestamp = fields.DateTime(dump_only=True)
    content = BytesField(allow_none=False, required=True)

    # relationships
    message_id = fields.Int(allow_none=False, required=True)

    @post_load
    def init_model(self, data):
        data["timestamp"] = datetime.utcnow()
        return Packet(**data)


class MessageSchema(Schema):
    # primary key and foreign keys
    id = fields.Int(dump_only=True)

    # table attributes
    message_number = fields.Int(allow_none=False, required=True)
    address = fields.String(allow_none=False, required=True)
    time_begin_sending = fields.DateTime(dump_only=True)
    time_done_sending = fields.DateTime()
    value_type = fields.String(allow_none=False, required=True)
    data_type = fields.String(allow_none=False, required=True)
    total_packets = fields.Integer(allow_none=False, required=True)
    done = fields.Boolean(dump_only=True)
    message_type = EnumField(MessageType, by_value=True, allow_none=False, required=True)

    @post_load
    def init_model(self, data):
        data["time_begin_sending"] = datetime.utcnow()
        return Message(**data)


class DataInSchema(Schema):
    address = fields.String(allow_none=True, required=True)
    data = fields.String(allow_none=False, required=True)


