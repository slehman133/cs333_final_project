import unittest
from samqlite import *


class HandleArgsTest(unittest.TestCase):
    def setUp(self):
        create_database("test")

    # integration tests 
    def test_handle_args_create_table(self):
        use_database("test")
        handle_args("create table table1 (example int)")
        self.assertTrue(os.path.exists("test/table1"))

    def test_handle_args_drop_table(self):
        use_database("test")
        create_table("table1 (example int)")
        handle_args("DROP TABLE table1")
        self.assertFalse(os.path.exists("test/table1"))

    def test_handle_args_drop_database(self):
        use_database("test")
        handle_args("DROP DATABASE test")
        self.assertFalse(os.path.exists("test"))

    def test_handle_args_insert_into_table(self):
        use_database("test")
        create_table("table1 (example int)")
        handle_args("insert into table1 values (1)")

        with open("test/table1", "r") as f:
            lines = f.readlines()
            self.assertEqual(lines[1], "1\n")

    def test_handle_args_alter_table(self):
        use_database("test")
        create_table("table1 (example int)")
        handle_args("ALTER table table1 add example2 int")
        with open("test/table1", "r") as f:
            lines = f.readlines()
            self.assertEqual(lines[0], "example int|example2 int\n")

    def tearDown(self):
        drop_database("test")
        
    