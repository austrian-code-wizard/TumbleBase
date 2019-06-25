from tumbleWeb.database.database import DatabaseConnector, DatabaseTools
from tumbleWeb.model.schema import ImageSchema, MessageSchema, CommandSchema
from tumbleWeb.businesslogic.busineslogic import TumbleWebLogic
from tumbleWeb.logger.logger import LoggerFactory
from tumbleWeb.tumbleweb_api import app
from tumbleWeb.util.mode import Mode
import unittest
import base64


class RestApiTest(unittest.TestCase):
    """
    def setUp(self):
        self.database_connector = DatabaseConnector()
        self.database_connector.connection_string = DatabaseConnector.get_connection_string(mode=Mode.test)
        self.database_connector.pool_size = DatabaseConnector.get_pool_size(mode=Mode.test)
        self.database_tools = DatabaseTools(self.database_connector)
        self.database_tools.drop_database()
        self.database_tools.create_database()
        self.database_tools.create_admin_user()

        self.app = app.test_client()
        self.app.testing = True

        self.app.application.config["FRANGLOMAT_LOGGER"] = LoggerFactory.create_logger("rest-api-test-logger")
        self.app.application.config["FRANGLOMAT_FRENCH_BUSINESS_LOGIC"] = \
            FrenchBusinessLogic.get_business_logic(Mode.test)
        self.app.application.config["FRANGLOMAT_USER_SCHEMA"] = FranglomatUserSchema()
        self.app.application.config["FRANGLOMAT_CATEGORY_SCHEMA"] = CategorySchema()

    def test_login(self):
        response = self.app.get("/login", headers={
            "Authorization": 'Basic ' + base64.b64encode(bytes("Hubster:password", 'ascii')).decode('ascii')
        })

        self.assertEqual(response.status, "200 OK")
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["username"], "Hubster")
        self.assertEqual(response.json["admin"], True)
        self.assertEqual(response.json["id"], 1)

    def tearDown(self):
        self.database_tools.drop_database()
        self.database_connector.engine.dispose()

"""
if __name__ == "__main__":
    unittest.test()
