import unittest
from samuellehman_pa4 import *


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        create_database("test")

    def test_create_database(self):
        create_database("test2")
        self.assertTrue(os.path.exists("test2"))

    def test_use_database(self):
        create_database("test")
        use_database("test")
        self.assertEqual(activeDB, ".")

    def test_drop_database(self):
        drop_database("test")
        self.assertFalse(os.path.exists("test"))

    def test_create_table(self):
        use_database("test")
        create_table("table1 (example int)")
        self.assertTrue(os.path.exists("test/table1"))

    def test_drop_table(self):
        use_database("test")
        create_table("table1 (example int)")
        drop_table("table1")
        self.assertFalse(os.path.exists("test/table1"))

    def test_select_from_tuple(self):
        use_database("test")
        create_table("table1 (example int)")
        insert_into("table1 values(1)")
        content = select_from_tuple("select * from table1")
        self.assertTrue(content, ['1'])

    def test_update_tuple(self):
        use_database("test")
        create_table("table1 (example int)")
        insert_into("table1 values(1)")
        update_tuple("table1 set example = 2 where example = 1")
        content = select_from_tuple("select * from table1")
        self.assertTrue(content, ['2'])

    def test_check_for_lock(self):
        use_database("test")
        create_table("table1 (example int)")
        insert_into("table1 values(1)")
        self.assertTrue(check_for_lock("table1"))
        

    def tearDown(self):
        drop_database("test")
        drop_database("test2")