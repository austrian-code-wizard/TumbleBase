from util.utils import internal_server_error_message, invalid_format_message, endpoint_not_found_message, \
    method_not_allowed_message, could_not_verify_message, invalid_token_message, no_admin_message
from exception.custom_exceptions import TumbleWebException, InternalServerError
from model.schema import ImageSchema, MessageSchema, CommandSchema
from businesslogic.busineslogic import TumbleWebLogic
from flask import Flask, request, jsonify
from logger.logger import LoggerFactory
from marshmallow import ValidationError
from functools import wraps


"""
Flask is built for extensions. Use the config to add new keywords and new resources which can be used in the
endpoint definitions. This is needed for example for testing. Now it is possible to connect a business logic
which is connected to a test database and everything runs over the app config.
"""

app = Flask(__name__)
app.config["TUMBLEWEB_LOGGER"] = LoggerFactory.create_logger("rest-api-logger")
app.config["TUMBLEWEB_BUSINESS_LOGIC"] = TumbleWebLogic.get_business_logic()
app.config["TUMBLEWEB_IMAGE_SCHEMA"] = ImageSchema()
app.config["TUMBLEWEB_MESSAGE_SCHEMA"] = MessageSchema()
app.config["TUMBLEWEB_COMMAND_SCHEMA"] = CommandSchema()


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
        except TumbleWebException as e:
            return jsonify({"info": str(e)}), 400
        except InternalServerError as e:
            return jsonify({"info": str(e)}), 500
        except Exception as e:
            app.config["TUMBLEWEB_LOGGER"].error("TumbleWebApi.handle_exception(): " + str(e))
            return jsonify({"info": internal_server_error_message}), 500
    return wrapper


@app.route("/add-message", methods=["POST"])
@handle_exception
def add_message():
    message_json = request.get_json()
    message_to_insert, errors = app.config["TUMBLEWEB_MESSAGE_SCHEMA"].load(message_json)
    message_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_message(message_to_insert)
    if message_id is None:
        return jsonify({"info": f"The message cannot be saved."}), 400
    else:
        return jsonify({"info": message_id})

@app.route("/add-and-send-command", methods=["POST"])
@handle_exception
def add_and_send_command():
    command_json = request.get_json()
    command_to_insert, errors = app.config["TUMBLEWEB_COMMAND_SCHEMA"].load(command_json)
    command_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_and_send_command(command_to_insert)
    if command_id is None:
        return jsonify({"info": f"The command cannot be saved or sent."}), 400
    else:
        return jsonify({"info": command_id})


@app.route("/add-image", methods=["POST"])
@handle_exception
def add_image():
    image_json = request.get_json()
    image_to_insert, errors = app.config["TUMBLEWEB_IMAGE_SCHEMA"].load(image_json)
    #TODO: Validate image data and save as file
    image_id = app.config["TUMBLEWEB_BUSINESS_LOGIC"].save_image(image_to_insert)
    if image_id is None:
        return jsonify({"info": f"The image cannot be saved."}), 400
    else:
        return jsonify({"info": image_id})


@app.route("/get-message/<int:message_id>", methods=["GET"])
@handle_exception
def get_message(message_id):
    found_message = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_message(message_id)
    if found_message is None:
        return jsonify({"info": f"The message with the id '{message_id}' does not exist."}), 400
    else:
        result, errors = app.config["TUMBLEWEB_MESSAGE_SCHEMA"].dump(found_message)
        return jsonify(result)


@app.route("/get-command/<int:command_id>", methods=["GET"])
@handle_exception
def get_command(command_id):
    found_command = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_command(command_id)
    if found_command is None:
        return jsonify({"info": f"The command with the id '{command_id}' does not exist."}), 400
    else:
        result, errors = app.config["TUMBLEWEB_COMMAND_SCHEMA"].dump(found_command)
        return jsonify(result)


@app.route("/get-image/<int:image_id>", methods=["GET"])
@handle_exception
def get_image(image_id):
    found_image = app.config["TUMBLEWEB_BUSINESS_LOGIC"].get_image(image_id)
    if found_image is None:
        return jsonify({"info": f"The image with the id '{image_id}' does not exist."}), 400
    else:
        #TODO: Load image from file and attach to json
        result, errors = app.config["TUMBLEWEB_IMAGE_SCHEMA"].dump(found_image)
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
