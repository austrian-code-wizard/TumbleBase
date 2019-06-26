from model.data_transfer_objects import Packet, Message
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from model.enums import MessageType
from datetime import datetime


class PacketSchema(Schema):
    # primary key and foreign keys
    id = fields.Int(dump_only=True)

    # table attributes
    packet_number = fields.Int(allow_none=False, required=True)
    timestamp = fields.DateTime(dump_only=True)
    content = fields.String(allow_none=False, required=True)

    # relationships
    message_id = fields.Int(allow_none=False, required=True)

    @post_load
    def init_model(self, data):
        data["timestamp"] = datetime.utcnow()
        return Packet(**data)


class MessageSchema(Schema):
    # primary key and foreign keys
    id= fields.Int(dump_only=True)

    # table attributes
    message_number = fields.Int(allow_none=False, required=True)
    address = fields.String(allow_none=False, required=True)
    time_begin_sending = fields.DateTime(dump_only=True)
    time_done_sending = fields.DateTime()
    type = fields.String(allow_none=False, required=True)
    value = fields.String(allow_none=False, required=True)
    done = fields.Boolean(allow_none=False, required=True)
    message_type = EnumField(MessageType, by_value=True, allow_none=False, required=True)

    # relationships
    # packets = fields.Nested(PacketSchema, dump_only=True) # TODO: Not sure if necessary

    @post_load
    def init_model(self, data):
        data["time_begin_sending"] = datetime.utcnow()
        return Message(**data)

