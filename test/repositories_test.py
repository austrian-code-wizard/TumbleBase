from tumbleWeb.repositories.repositories import MessageRepository, ImageRepository, CommandRepository
from tumbleWeb.model.data_access_objects import Message, Image, Command
from tumbleWeb.database.database import DatabaseConnector, DatabaseTools
from sqlalchemy.exc import IntegrityError, DataError
from tumbleWeb.util.mode import Mode
import unittest
import datetime


# TODO: test aren't working under ubuntu, have to fix this bug
class RepositoriesTest(unittest.TestCase):
    """
    def setUp(self):
        self.database_connector = DatabaseConnector()
        self.database_connector.connection_string = DatabaseConnector.get_connection_string(mode=Mode.test)
        self.database_connector.pool_size = DatabaseConnector.get_pool_size(mode=Mode.test)
        self.database_tools = DatabaseTools(self.database_connector)
        self.database_tools.drop_database()
        self.database_tools.create_database()

        self.franglomat_user_repository = FranglomatUserRepository.get_repository()
        self.vocabulary_repository = VocabularyRepository.get_repository()
        self.french_vocabulary_repository = FrenchVocabularyRepository.get_repository()
        self.french_noun_repository = FrenchNounRepository.get_repository()
        self.category_repository = CategoryRepository.get_repository()

    def tearDown(self):
        self.database_tools.drop_database()
        self.database_connector.engine.dispose()

    def test_basic_save_get_delete(self):
        session = self.database_connector.session
        franglomat_user = FranglomatUser(id=1, username="herbert", password="password")
        franglomat_user_id = self.franglomat_user_repository.save_entity(franglomat_user, session)
        self.assertEqual(franglomat_user_id, 1)
        session.close()

        session = self.database_connector.session
        franglomat_user = FranglomatUser(id=1, username="herbert", password="password")
        franglomat_user_id = self.franglomat_user_repository.save_entity(franglomat_user, session)
        self.assertEqual(franglomat_user_id, 1)
        session.close()

        session = self.database_connector.session
        franglomat_user = FranglomatUser(username="herbert", password="password")
        with self.assertRaises(IntegrityError):
            self.franglomat_user_repository.save_entity(franglomat_user, session)
        session.close()

        session = self.database_connector.session
        franglomat_user = FranglomatUser(username="sebastian", password="password")
        franglomat_user_id = self.franglomat_user_repository.save_entity(franglomat_user, session)
        self.assertEqual(franglomat_user_id, 2)
        session.close()

        session = self.database_connector.session
        franglomat_user = self.franglomat_user_repository.get_entity(2, session)
        self.assertIsInstance(franglomat_user, FranglomatUser)
        self.assertEqual(franglomat_user.id, 2)
        self.assertEqual(franglomat_user.username, "sebastian")
        self.assertEqual(franglomat_user.password, "password")
        session.close()

        session = self.database_connector.session
        franglomat_user_list = self.franglomat_user_repository.get_entities(session)
        self.assertIsInstance(franglomat_user_list, list)
        self.assertEqual(franglomat_user_list[0].id, 1)
        self.assertEqual(franglomat_user_list[0].username, "herbert")
        self.assertEqual(franglomat_user_list[0].password, "password")
        self.assertEqual(franglomat_user_list[1].id, 2)
        self.assertEqual(franglomat_user_list[1].username, "sebastian")
        self.assertEqual(franglomat_user_list[1].password, "password")
        session.close()

        session = self.database_connector.session
        wrong_data_type = "eins"
        with self.assertRaises(DataError):
            self.franglomat_user_repository.delete_entity(wrong_data_type, session)
        session.close()

        session = self.database_connector.session
        wrong_id = 3
        was_franglomat_user_deleted = self.franglomat_user_repository.delete_entity(wrong_id, session)
        self.assertFalse(was_franglomat_user_deleted)
        session.close()

        session = self.database_connector.session
        was_franglomat_user_deleted = self.franglomat_user_repository.delete_entity(2, session)
        self.assertTrue(was_franglomat_user_deleted)
        was_franglomat_user_deleted = self.franglomat_user_repository.delete_entity(1, session)
        self.assertTrue(was_franglomat_user_deleted)
        session.close()

    def test_save_for_every_model_class(self):
        # test for inserting a franglomat user
        session = self.database_connector.session
        franglomat_user = FranglomatUser(id=1, username="patrik", password="password")
        result_id = self.franglomat_user_repository.save_entity(franglomat_user, session)
        self.assertEqual(result_id, 1)
        session.close()

        # test for inserting a vocabulary
        session = self.database_connector.session
        vocabulary = Vocabulary(id=1, created_at=datetime.datetime.now())
        result_id = self.vocabulary_repository.save_entity(vocabulary, session)
        self.assertEqual(result_id, 1)
        session.close()

        # test for inserting a french vocabulary
        session = self.database_connector.session
        french_vocabulary = FrenchVocabulary(id=2, created_at=datetime.datetime.now(), french_word="la nuit",
                                             native_word="die Nacht")
        result_id = self.french_vocabulary_repository.save_entity(french_vocabulary, session)
        self.assertEqual(result_id, 2)
        session.close()

        # test for updating the french vocabulary
        session = self.database_connector.session
        french_vocabulary = FrenchVocabulary(id=2, created_at=datetime.datetime.now(), french_word="la bonne nuit",
                                             native_word="die gute Nacht")
        result_id = self.french_vocabulary_repository.save_entity(french_vocabulary, session)
        self.assertEqual(result_id, 2)
        session.close()

        # test for inserting a french noun
        session = self.database_connector.session
        french_noun = FrenchNoun(id=3, created_at=datetime.datetime.now(), french_word="la nuit",
                                 native_word="die Nacht", gender=Gender.feminin, numerus=Numerus.singular)
        result_id = self.french_noun_repository.save_entity(french_noun, session)
        self.assertEqual(result_id, 3)
        session.close()

        # test for inserting a category
        session = self.database_connector.session
        category = Category(id=1, category_name="le sport")
        result_id = self.category_repository.save_entity(category, session)
        self.assertEqual(result_id, 1)
        session.close()
"""

if __name__ == "__main__":
    unittest.test()
