from tumbleWeb.model.data_transfer_objects import Image, Message, Command
from marshmallow import Schema, fields, post_load
from datetime import datetime


class ImageSchema(Schema):

    id = fields.Int(dump_only=True)

    image_path = fields.String(allow_none=False, required=True)
    saved_at = fields.DateTime(dump_only=True)

    @post_load
    def init_model(self, data):
        data["saved_at"] = datetime.utcnow()
        return Image(**data)


class CommandSchema(Schema):

    id = fields.Int(dump_only=True)

    command = fields.String(allow_none=False, required=True)
    arguments = fields.String(allow_none=False, required=True)
    saved_at = fields.DateTime(dump_only=True)

    @post_load
    def init_model(self, data):
        data["saved_at"] = datetime.utcnow()
        return Command(**data)


class MessageSchema(Schema):

    id = fields.Int(dump_only=True)

    message = fields.String(allow_none=False, required=True)
    saved_at = fields.DateTime(dump_only=True)

    @post_load
    def init_model(self, data):
        data["saved_at"] = datetime.utcnow()
        return Message(**data)
