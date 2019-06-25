from tumbleWeb.model.data_access_objects import Message, Command, Image
from tumbleWeb.util.utils import internal_server_error_message, get_config_parser
from tumbleWeb.repositories.repositories import ImageRepository, CommandRepository, MessageRepository
from tumbleWeb.exception.custom_exceptions import TumbleWebException, InternalServerError
from tumbleWeb.model.data_transfer_objects import Message as MessageDto, Command as CommandDto, Image as ImageDto
from tumbleWeb.database.database import DatabaseConnector
from tumbleWeb.logger.logger import LoggerFactory
from abc import abstractmethod
from functools import wraps
from tumbleWeb.util.mode import Mode


def execute_in_session(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            business_logic = args[0]
            session = business_logic._database_connector.session
            kwargs["session"] = session

            # execute the method which needs the session
            result = func(*args, **kwargs)

            session.commit()
            return result
        except TumbleWebException as e:
            session.rollback()
            raise e
        except Exception as e:
            business_logic._logger.error(business_logic.__class__.__name__ + "." + func.__name__ + "(): " + str(e))
            session.rollback()
            raise InternalServerError(internal_server_error_message)
        finally:
            session.close()
    return wrapper


class BusinessLogic:

    def __init__(self, database_connector, logger, mode):
        self._database_connector = database_connector
        self._logger = logger
        self._mode = mode

    @staticmethod
    @abstractmethod
    def get_business_logic():
        raise NotImplementedError("You called an abstract method!")


# TODO: Restructuring business logic. Methods have to be moved into separate classes.
class TumbleWebLogic(BusinessLogic):

    def __init__(self, database_connector, logger, mode):
        super().__init__(database_connector, logger, mode)
        self._image_repository = None
        self._message_repository = None
        self._command_repository = None
        self._secret_key = None

    @property
    def image_repository(self):
        if self._image_repository is None:
            self._image_repository = ImageRepository.get_repository(self._mode)
        return self._image_repository

    @property
    def message_repository(self):
        if self._message_repository is None:
            self._message_repository = MessageRepository.get_repository(self._mode)
        return self._message_repository

    @property
    def command_repository(self):
        if self._command_repository is None:
            self._command_repository = CommandRepository.get_repository(self._mode)
        return self._command_repository

    @property
    def secret_key(self):
        if self._secret_key is None:
            environment_parser = get_config_parser("environment.ini")
            self._secret_key = environment_parser["environment"]["secret_key"]
        return self._secret_key

    @staticmethod
    def get_business_logic(mode=Mode.productive):
        database_connector = DatabaseConnector()
        database_connector.connection_string = DatabaseConnector.get_connection_string(mode=mode)
        if mode == Mode.productive:
            logger_name = "tumbleweb-business-logic-logger"
        elif mode == Mode.test:
            logger_name = "tumbleweb-business-logic-test-logger"
        logger = LoggerFactory.create_logger(logger_name)
        return TumbleWebLogic(database_connector, logger, mode)


    @execute_in_session
    def save_image(self, image_dto, session=None):
        image_dao = Image.create_from_dto(image_dto)
        image_id = self.image_repository.save_entity(image_dao, session)
        return image_id

    @execute_in_session
    def save_message(self, message_dto, session=None):
        message_dao = Message.create_from_dto(message_dto)
        message_id = self.image_repository.save_entity(message_dao, session)
        return message_id

    @execute_in_session
    def save_and_send_command(self, command_dto, session=None):
        command_dao = Command.create_from_dto(command_dto)
        command_id = self.image_repository.save_entity(command_dao, session)
        #TODO: Send command to transceiver base station
        return command_id

    @execute_in_session
    def get_image(self, image_id, session=None):
        image_dao = self.image_repository.get_entity(image_id, session)
        if image_dao is not None:
            image_dto = ImageDto.create_from_dao(image_dao)
            return image_dto
        else:
            return None

    @execute_in_session
    def get_message(self, message_id, session=None):
        message_dao = self.message_repository.get_entity(message_id, session)
        if message_dao is not None:
            message_dto = MessageDto.create_from_dao(message_dao)
            return message_dto
        else:
            return None

    @execute_in_session
    def get_command(self, command_id, session=None):
        command_dao = self.command_repository.get_entity(command_id, session)
        if command_dao is not None:
            command_dto = CommandDto.create_from_dao(command_dao)
            return command_dto
        else:
            return None
