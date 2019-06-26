from model.data_access_objects import Message, Packet
from util.utils import internal_server_error_message, get_config_parser
from repositories.repositories import PacketRepository, MessageRepository
from exception.custom_exceptions import TumbleBaseException, InternalServerError
from model.data_transfer_objects import Message as MessageDto, Packet as PacketDto
from database.database import DatabaseConnector
from logger.logger import LoggerFactory
from abc import abstractmethod
from functools import wraps
from util.mode import Mode
from datetime import datetime


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
        except TumbleBaseException as e:
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
class TumbleBaseLogic(BusinessLogic):

    def __init__(self, database_connector, logger, mode):
        super().__init__(database_connector, logger, mode)
        self._message_repository = None
        self._packet_repository = None
        self._secret_key = None

    @property
    def message_repository(self):
        if self._message_repository is None:
            self._message_repository = MessageRepository.get_repository(self._mode)
        return self._message_repository

    @property
    def packet_repository(self):
        if self._packet_repository is None:
            self._packet_repository = PacketRepository.get_repository(self._mode)
        return self._packet_repository

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
        return TumbleBaseLogic(database_connector, logger, mode)

    @execute_in_session
    def save_message(self, message_dto, session=None):
        message_dao = Message.create_from_dto(message_dto)
        message_id = self.message_repository.save_entity(message_dao, session)
        return message_id

    @execute_in_session
    def save_packet(self, packet_dto, session=None):
        packet_dao = Packet.create_from_dto(packet_dto)
        packet_id = self.packet_repository.save_entity(packet_dao, session)
        return packet_id

    @execute_in_session
    def get_message(self, message_id, session=None):
        message_dao = self.message_repository.get_entity(message_id, session)
        if message_dao is not None:
            message_dto = MessageDto.create_from_dao(message_dao)
            return message_dto
        else:
            return None

    @execute_in_session
    def get_packet(self, packet_id, session=None):
        packet_dao = self.packet_repository.get_entity(packet_id, session)
        if packet_dao is not None:
            packet_dto = PacketDto.create_from_dao(packet_dao)
            return packet_dto
        else:
            return None

    @execute_in_session
    def get_messages(self, session=None):
        messages_dao = self.message_repository.get_entities(session)
        if messages_dao is not None:
            messages_dto = MessageDto.create_from_dao_list(messages_dao)
            return messages_dto
        else:
            return None

    @execute_in_session
    def get_packets(self, session=None):
        packets_dao = self.packet_repository.get_entities(session)
        if packets_dao is not None:
            packets_dto = PacketDto.create_from_dao_list(packets_dao)
            return packets_dto
        else:
            return None

    @execute_in_session
    def set_message_to_done(self, message_id, session=None):
        message_dao = self.message_repository.get_entity(message_id, session)
        message_dao.time_done_sending = datetime.utcnow()
        message_dao.done = True
        message_id = self.message_repository.save_entity(message_dao, session)
        return message_id

