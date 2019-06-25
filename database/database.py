from sqlalchemy.orm.session import sessionmaker
from tumbleWeb.model.data_access_objects import Base
from tumbleWeb.util.utils import get_config_parser
from sqlalchemy import create_engine
from tumbleWeb.util.mode import Mode

Session = sessionmaker(autoflush=True)


class DatabaseConnector:

    def __init__(self):
        self._engine = None
        self._connection_string = None
        self._pool_size = 10

    @staticmethod
    def get_connection_string(mode=Mode.productive):
        config_parser = get_config_parser("database.ini")

        database_type = config_parser[mode.value]["database_type"]
        username = config_parser[mode.value]["username"]
        password = config_parser[mode.value]["password"]
        host = config_parser[mode.value]["host"]
        port = config_parser[mode.value]["port"]
        database = config_parser[mode.value]["database"]

        return f"{database_type}://{username}:{password}@{host}:{port}/{database}"

    @staticmethod
    def get_pool_size(mode=Mode.productive):
        config_parser = get_config_parser("database.ini")
        return int(config_parser[mode.value]["pool_size"])

    @property
    def pool_size(self):
        return self._pool_size

    @pool_size.setter
    def pool_size(self, new_value):
        self._pool_size = new_value

    @property
    def connection_string(self):
        return self._connection_string

    @connection_string.setter
    def connection_string(self, new_value):
        self._connection_string = new_value

    def create_engine(self):
        # echo=True prints all statements executed on the database
        self._engine = create_engine(self._connection_string, pool_size=self._pool_size)
        Session.configure(bind=self._engine)
        return self._engine

    @property
    def engine(self):
        if self._engine is None:
            self.create_engine()
        return self._engine

    @property
    def session(self):
        if self._engine is None:
            self.create_engine()
        return Session()


class DatabaseTools:

    def __init__(self, database_connector):
        self._database_connector = database_connector

    def create_database(self):
        Base.metadata.create_all(bind=self._database_connector.engine)

    def drop_database(self):
        Base.metadata.drop_all(bind=self._database_connector.engine)


if __name__ == "__main__":
    database_connector = DatabaseConnector()
    database_connector.connection_string = DatabaseConnector.get_connection_string()
    database_connector.pool_size = DatabaseConnector.get_pool_size()
    database_tools = DatabaseTools(database_connector)

    print(">>> create and drop database")
    database_tools.drop_database()
    print(">>> dropped database")
    print("-----------------------------------------------------------------------------------------------------------")

    database_tools.create_database()
    print(">>> create database")
    print(">>> successfully set up new database")
    print("-----------------------------------------------------------------------------------------------------------")

    database_connector.engine.dispose()
