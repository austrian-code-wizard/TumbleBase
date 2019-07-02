from util.utils import internal_server_error_message, invalid_format_message, endpoint_not_found_message, \
    method_not_allowed_message, could_not_verify_message, invalid_token_message, no_admin_message
from exception.custom_exceptions import TumbleBaseException, InternalServerError
from model.schema import MessageSchema, PacketSchema, DataInSchema
from businesslogic.busineslogic import TumbleBaseLogic
from flask import Flask, request, jsonify
from logger.logger import LoggerFactory
from marshmallow import ValidationError
from model.enums import MessageType
from functools import wraps
from twClasses.twParser import Parser
from twClasses.twXBee import XBee
from twClasses.twWebConnector import twWebConnector

# TODO: Message format: 4 message, 2 packet id, 2 number of packets, 1 data type, 2 datapoint id, rest is packet data

"""
Flask is built for extensions. Use the config to add new keywords and new resources which can be used in the
endpoint definitions. This is needed for example for testing. Now it is possible to connect a business logic
which is connected to a test database and everything runs over the app config.
"""

app = Flask(__name__)
app.config["TUMBLEBASE_LOGGER"] = LoggerFactory.create_logger("rest-api-logger")
app.config["TUMBLEBASE_BUSINESS_LOGIC"] = TumbleBaseLogic.get_business_logic()
app.config["TUMBLEBASE_MESSAGE_SCHEMA"] = MessageSchema()
app.config["TUMBLEBASE_PACKET_SCHEMA"] = PacketSchema()
app.config["TUMBLEBASE_DATAINSCHEMA_SCHEMA"] = DataInSchema()
app.config["TUMBLEBASE_TRANSCEIVER_DEVICE"] = XBee("/dev/tty.usbserial-1420")
app.config["TUMBLEBASE_MESSAGE_PARSER"] = Parser()
app.config["TUMBLEBASE_TUMBLEWEB_CONNECTOR"] = twWebConnector()


@app.errorhandler(404)
def page_not_found(_):
    return jsonify({"info": endpoint_not_found_message}), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"info": method_not_allowed_message}), 405


def handle_exception(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValidationError:
            return jsonify({"info": invalid_format_message}), 400
        except TumbleBaseException as e:
            return jsonify({"info": str(e)}), 400
        except InternalServerError as e:
            return jsonify({"info": str(e)}), 500
        except Exception as e:
            app.config["TUMBLEBASE_LOGGER"].error("TumbleWebApi.handle_exception(): " + str(e))
            return jsonify({"info": internal_server_error_message}), 500
    return wrapper


@app.route("/add-message", methods=["POST"])
@handle_exception
def add_message():
    message_json = request.get_json()
    message_to_insert = app.config["TUMBLEBASE_MESSAGE_SCHEMA"].load(message_json)
    message_id = app.config["TUMBLEBASE_BUSINESS_LOGIC"].save_message(message_to_insert)
    if message_id is None:
        return jsonify({"info": f"The message cannot be saved."}), 400
    else:
        return jsonify({"info": message_id})


def process_incoming_message(data):
    """def process_incoming_message(data):
    address = data.remote_device.get_64bit_addr()
    data = data.data"""

    #  for testing
    """message_json = request.get_json()
    message_json = app.config["TUMBLEBASE_DATAINSCHEMA_SCHEMA"].load(message_json)
    address = message_json["address"]
    data = message_json["data"]
    sending_packets = app.config["TUMBLEBASE_MESSAGE_PARSER"].prepare_command(data)
    data = sending_packets[0]
    data = b'\x00\x00\x00\x01\x00\x01\x00\x01dT1@9\xad\x91hr\xb0!'
    address = "1234567654321"""
    data = data.to_dict()
    address = data["Sender: "]
    data = data["Data: "]
    message = app.config["TUMBLEBASE_MESSAGE_PARSER"].parse_message(data)
    message["address"] = address
    packet = app.config["TUMBLEBASE_MESSAGE_PARSER"].parse_packet(data)

    message["message_type"] = MessageType.message
    message_id = app.config["TUMBLEBASE_BUSINESS_LOGIC"].find_unfinished_message(message["address"],
                                                                                 message["message_number"],
                                                                                 message["value_type"])
    if message_id is None:
        message_to_insert = app.config["TUMBLEBASE_MESSAGE_SCHEMA"].load(message)
        message_id = app.config["TUMBLEBASE_BUSINESS_LOGIC"].save_message(message_to_insert)
    packet["message_id"] = message_id
    packet_to_insert = app.config["TUMBLEBASE_PACKET_SCHEMA"].load(packet)
    app.config["TUMBLEBASE_BUSINESS_LOGIC"].save_packet(packet_to_insert)
    if app.config["TUMBLEBASE_BUSINESS_LOGIC"].message_complete(message_id):
        app.config["TUMBLEBASE_BUSINESS_LOGIC"].set_message_to_done(message_id)
        found_message = app.config["TUMBLEBASE_BUSINESS_LOGIC"].get_message(message_id)
        found_packets = app.config["TUMBLEBASE_BUSINESS_LOGIC"].get_packets_by_message_id(message_id)
        value = b''
        result = app.config["TUMBLEBASE_MESSAGE_SCHEMA"].dump(found_message)
        for p in found_packets:
            value += p.content
        result["value"] = app.config["TUMBLEBASE_MESSAGE_PARSER"].convert_value_from_bytes(value, result["data_type"])
        return jsonify(app.config["TUMBLEBASE_TUMBLEWEB_CONNECTOR"].send(result))
    return jsonify({"id": message_id})


app.config["TUMBLEBASE_TRANSCEIVER_DEVICE"].set_callback(process_incoming_message)


@app.route("/send-command", methods=["POST"])
@handle_exception
def sent_command():
    message_json = request.get_json()
    message_json = app.config["TUMBLEBASE_DATAINSCHEMA_SCHEMA"].load(message_json)
    address = message_json["address"]
    data = message_json["data"]
    sending_packets = app.config["TUMBLEBASE_MESSAGE_PARSER"].prepare_command(data)
    saving_message = app.config["TUMBLEBASE_MESSAGE_PARSER"].parse_message(sending_packets[0])
    saving_message["address"] = address
    saving_message["message_type"] = MessageType.command
    message_to_insert = app.config["TUMBLEBASE_MESSAGE_SCHEMA"].load(saving_message)
    message_id = app.config["TUMBLEBASE_BUSINESS_LOGIC"].save_message(message_to_insert)
    for p in sending_packets:
        app.config["TUMBLEBASE_TRANSCEIVER_DEVICE"].write(p, address)
        packet_json = app.config["TUMBLEBASE_MESSAGE_PARSER"].parse_packet(p)
        packet_json["message_id"] = message_id
        packet_to_insert = app.config["TUMBLEBASE_PACKET_SCHEMA"].load(packet_json)
        app.config["TUMBLEBASE_BUSINESS_LOGIC"].save_packet(packet_to_insert)
    app.config["TUMBLEBASE_BUSINESS_LOGIC"].set_message_to_done(message_id)
    return jsonify({"info": message_id})


@app.route("/add-packet", methods=["POST"])
@handle_exception
def add_packet():
    packet_json = request.get_json()
    packet_to_insert = app.config["TUMBLEBASE_PACKET_SCHEMA"].load(packet_json)
    packet_id = app.config["TUMBLEBASE_BUSINESS_LOGIC"].save_packet(packet_to_insert)
    if packet_id is None:
        return jsonify({"info": f"The packet cannot be saved."}), 400
    else:
        return jsonify({"info": packet_id})


@app.route("/get-message/<int:message_id>", methods=["GET"])
@handle_exception
def get_message(message_id):
    found_message = app.config["TUMBLEBASE_BUSINESS_LOGIC"].get_message(message_id)
    if found_message is None:
        return jsonify({"info": f"The message with the id '{message_id}' does not exist."}), 400
    else:
        result = app.config["TUMBLEBASE_MESSAGE_SCHEMA"].dump(found_message)
        return jsonify(result)


@app.route("/get-packet/<int:packet_id>", methods=["GET"])
@handle_exception
def get_packet(packet_id):
    found_packet = app.config["TUMBLEBASE_BUSINESS_LOGIC"].get_packet(packet_id)
    if found_packet is None:
        return jsonify({"info": f"The packet with the id '{packet_id}' does not exist."}), 400
    else:
        result = app.config["TUMBLEBASE_PACKET_SCHEMA"].dump(found_packet)
        result["content"] = str(result["content"])
        return jsonify(result)


@app.route("/get-messages", methods=["GET"])
@handle_exception
def get_messages():
    found_messages = app.config["TUMBLEBASE_BUSINESS_LOGIC"].get_messages()
    if found_messages is None:
        return jsonify({"info": f"No messages exist."}), 400
    else:
        result = app.config["TUMBLEBASE_MESSAGE_SCHEMA"].dump(found_messages, many=True)
        return jsonify(result)


@app.route("/get-packets", methods=["GET"])
@handle_exception
def get_packets():
    found_packets = app.config["TUMBLEBASE_BUSINESS_LOGIC"].get_packets()
    if found_packets is None:
        return jsonify({"info": f"No packet was found."}), 400
    else:
        result = app.config["TUMBLEBASE_PACKET_SCHEMA"].dump(found_packets, many=True)
        for r in result:
            r["content"] = str(r["content"])
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8002")
