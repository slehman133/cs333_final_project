import unittest
from samqlite import *
from SamQLTable import *


class SamQLTableTest(unittest.TestCase):
    def setUp(self):
        create_database("test")

    def test_read_table_file(self):
        handle_args("use test")
        handle_args("create table table1 (example int)")
        handle_args("insert into table1 values (1)")
        table = SamQLTable("test", "table1")
        content = table.read_table_file(table.tablePath)
        self.assertEqual(content, ['example int', '2'])

    def test_update_table_file(self):
        handle_args("use test")
        handle_args("create table table1 (example int)")
        handle_args("insert into table1 values (1)")
        table = SamQLTable("test", "table1")
        table.update_table("set example = 2 where example = 1")
        content = table.read_table_file(table.tablePath)
        self.assertEqual(content, ['example int', '2'])

    def test_delete_from_table_file(self):
        handle_args("use test")
        handle_args("create table table1 (example int)")
        handle_args("insert into table1 values (1)")
        table = SamQLTable("test", "table1")
        table.delete_from_table("example = 1")
        content = table.read_table_file(table.tablePath)
        self.assertEqual(content, ['example int'])

    def test_insert_into_table_file(self):
        handle_args("use test")
        handle_args("create table table1 (example int)")
        table = SamQLTable("test", "table1")
        table.insert_into("1")
        content = table.read_table_file(table.tablePath)
        self.assertEqual(content, ['example int', '1'])

    def test_select_from_table_file(self):
        handle_args("use test")
        handle_args("create table table1 (example int)")
        handle_args("insert into table1 values (1)")
        handle_args("insert into table1 values (2)")
        handle_args("insert into table1 values (3)")
        table = SamQLTable("test", "table1")
        content = table.select_from_table("select example from table1")
        self.assertEqual(content, ['example int', '1', '2', '3'])

    def test_drop_table(self):
        handle_args("use test")
        handle_args("create table table1 (example int)")
        handle_args("insert into table1 values (1)")
        table = SamQLTable("test", "table1")
        table.drop_table()
        self.assertFalse(os.path.exists("test/table1"))


    def tearDown(self):
        drop_database("test")
    
