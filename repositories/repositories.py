from tumbleWeb.model.data_access_objects import Image, Message, Command
from tumbleWeb.logger.logger import LoggerFactory
from abc import abstractmethod
from tumbleWeb.util.mode import Mode
from re import findall


class Repository:
    """
    There exists repositories and daos. The difference between these two is a dao builds sql commands and executes them
    on the database like the sqlalchemy orm does for us. A repository uses a dao to store and load data. The better way
    to explain it is with anemic and rich models. Rich models include also data access to the database. Anemic models
    only describe the structure of data in the database. A repository uses a rich model to query and insert data into
    the database. A dao uses a anemic model to create sql commands and communicate with the database. So in this case
    it is a repository with a rich sqlalchemy model.
    """
    def __init__(self, logger, entity_model):
        self._logger = logger
        self.entity_model = entity_model

    def save_entity(self, entity, session):
        entity = session.merge(entity)
        session.commit()
        return entity.id

    def get_entity(self, entity_id, session):
        return session.query(self.entity_model).filter(self.entity_model.id == entity_id).first()

    def get_entities(self, session):
        return session.query(self.entity_model).order_by(self.entity_model.id).all()

    @abstractmethod
    def delete_entity(self, entity_id, session):
        raise NotImplementedError("You called an abstract method!")

    @classmethod
    def get_repository(cls, mode=Mode.productive):
        """
        Instantiate a logger named after the given class. The name of the logger is derived
        from the class name by adding "-" signs between all parts of the camelcased name.
        See https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
        for the respective regular expression. Create and return the instantiated class.
        :param mode: Describes if the application is run in productive or test mode.
        :return: A newly instantiated class that is connected to the logger.
        """
        parts = findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', cls.__name__)
        name = "-".join([s.lower() for s in parts])
        if mode == Mode.productive:
            logger_name = f"{name}-logger"
        if mode == Mode.test:
            logger_name = f"{name}-test-logger"
        logger = LoggerFactory.create_logger(logger_name)
        return cls(logger)


class ImageRepository(Repository):
    """
    A repository for Images.
    """

    def __init__(self, logger):
        super().__init__(logger, Image)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class MessageRepository(Repository):

    def __init__(self, logger):
        super().__init__(logger, Message)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")


class CommandRepository(Repository):

    def __init__(self, logger):
        super().__init__(logger, Command)

    def delete_entity(self, entity_id, session):
        raise NotImplementedError("Not available!")

