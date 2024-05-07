# Samuel Lehman
# CS457
# 31 October 2022
# Project 4 for CS457

import os
import sys
import subprocess
from SamQLTable import SamQLTable

activeDB = "."
quit = False
transacting = False
transaction_table = None
transaction_client = False
transaction_table = [""]


def main() -> None:
    """
    entry point of the program
    """
    # print("HELLLOOOOOO")
    if (len(sys.argv) > 1):
        handle_prog_args()

    while (quit == False):
        args = input("SamQLite> ").split(";")
        for arg in args:
            handle_args(arg)


def handle_prog_args() -> None:
    """
    takes the second argument as the file name and reads
    that file then sends that to the handle_args function
    """
    fileName = sys.argv[1]
    if (os.path.exists(fileName)):
        fileInput = []
        with open(fileName, "r") as file:
            for line in file:
                fileInput.append(line)
        args = "".join(fileInput).strip().split(";")
        for arg in args:
            handle_args(arg.strip())
    else:
        print(f"ERROR: File {fileName} does not exist")


def handle_prog_args_from_file(fileName: str) -> None:
    """
    used to take sql commands from a file while in program
    """
    if (os.path.exists(fileName)):
        fileInput = []
        with open(fileName, "r") as file:
            for line in file:
                fileInput.append(line)
        args = "".join(fileInput).strip().split(";")
        for arg in args:
            handle_args(arg.strip())
    else:
        print(f"ERROR: File {fileName} does not exist")


def handle_args(arg: str) -> None:
    """
    takes the commands and arguments from input and sends them
    to the corresponding function
    """
    # database functions
    if (arg.__contains__("CREATE DATABASE")):
        create_database(arg.removeprefix("CREATE DATABASE").strip())
    elif (arg.__contains__("DROP DATABASE")):
        drop_database(arg.removeprefix("DROP DATABASE").strip())
    elif (arg.__contains__("USE")):
        use_database(arg.removeprefix("USE").strip())
    # table functions
    elif (arg.__contains__("CREATE TABLE") or arg.__contains__("create table")):
        create_table(arg.removeprefix(
            "CREATE TABLE").removeprefix("create table").strip())
    elif (arg.__contains__("DROP TABLE")):
        drop_table(arg.removeprefix("DROP TABLE ").strip())
    elif (arg.__contains__("ALTER")):
        alter_table(arg.removeprefix("ALTER").strip())
    # tuple functions
    elif (arg.__contains__("select")):
        tables = select_from_tuple(arg.strip())
        return tables
    elif (arg.__contains__("insert into")):
        insert_into(arg.removeprefix("insert into").strip())
    elif (arg.__contains__("update")):
        update_tuple(arg.removeprefix("update").strip())
    elif (arg.__contains__("delete")):
        delete_tuple(arg.removeprefix("delete").strip())
    elif (arg.__contains__("begin transaction")):
        handle_transaction()
    elif (arg.__contains__("commit")):
        handle_commit()
    elif (arg.__contains__(".sql")):
        handle_prog_args_from_file(arg)
    else:
        if (arg.__contains__("EXIT") or arg.__contains__(".EXIT")
                or arg.__contains__(".exit")):
            global quit
            quit = True
            print("All done.")
        elif (arg != ""):
            print(f"Unknown command: {arg}")


def create_database(data: str) -> None:
    """
    handles the creation of databases
    """
    if (os.path.exists(data) == True):
        print(f"ERROR: Database {data} exists")
    else:
        subprocess.run(["mkdir", data])
        print(f"Created database {data}")


def drop_database(data: str) -> None:
    """
    handles the deletion of databases
    """

    if (os.path.exists(data) == True):
        subprocess.run(["rm", "-r", data])
        print(f"Dropped database {data}")
    else:
        print(f"ERROR: No database named {data}")


def use_database(data: str) -> None:
    """
    sets the current working database
    """
    if (os.path.exists(data) == True):
        global activeDB
        activeDB = os.path.abspath(data)
        print(f"Active database: {data}")
    else:
        print(f"ERROR: No database named {data} exists")


def create_table(data: str) -> None:
    """
    handles table creation
    """
    tableName = data.split()[0].strip()[:data.find('(')]
    # parses the data between ( )
    args = data[data.find('(')+1:data.rfind(')')]
    table = SamQLTable(activeDB, tableName, args)
    del table


def drop_table(data: str) -> None:
    """
    handles table deletion
    """
    tableName = data
    table = SamQLTable(activeDB, tableName)
    table.drop_table()
    del table


def alter_table(data: str) -> None:
    """
    handles altering data in tables
    """
    tableName = data.split()[1]
    fileInput = "|" + " ".join(data.split()[3:])
    print(fileInput)
    table = SamQLTable(activeDB, tableName)
    table.alter_table(fileInput)
    del table


def select_from_tuple(data: str)->list:
    """
    handles getting data from tables
    """
    # gets tableName from data
    tableName = data.split()[data.split().index("from")+1]
    fromTables = get_join_tables(data.split("\n"))
    if (data.__contains__("*") and len(fromTables) > 1):
        tables = []
        for table in fromTables:
            tables.append(SamQLTable(activeDB, table.replace("'", "")))

        print("TABLES   ",tables)

        columns, operation = get_where_on(data)

        # left outer join
        if (data.__contains__("left outer join")):
            print(tables[0].columns.replace(
                "|", " | ") + " | " + tables[1].columns.replace(
                "|", " | "))

            for line1 in tables[0].rows:
                line2_ids = []
                for line2 in tables[1].rows:
                    if (operation == "="):
                        # checking the indicies where the columns are located in
                        # their respective tables
                        if (line1.split("|")[tables[0].get_column_index(columns[0])]
                                == line2.split("|")[tables[1].get_column_index(columns[1])]):
                            line2_ids.append(line2.split("|")[0])
                            print(line1.replace(
                                "|", " | ") + " | " + line2.replace(
                                "|", " | "))
                if (line1.split("|")[0] not in line2_ids):
                    print(line1.replace(
                        "|", " | ") + " | | ")
        else:
            # inner join
            print(tables[0].columns.replace(
                "|", " | ") + " | " + tables[1].columns.replace(
                "|", " | "))
            for line1 in tables[0].rows:
                for line2 in tables[1].rows:
                    if (operation == "="):
                        # checking the indicies where the columns are located in
                        # their respective tables
                        if (line1.split("|")[tables[0].get_column_index(columns[0])]
                                == line2.split("|")[tables[1].get_column_index(columns[1])]):
                            print(line1.replace(
                                "|", " | ") + " | " + line2.replace(
                                "|", " | "))
        return tables
        del tables
    else:
        table = SamQLTable(activeDB, tableName)
        table.print_table()
        return table.rows
    del table


def get_where_on(data: str) -> list:
    """
    returns the columns and the comparison operation from the
    join statement
    """
    values = None
    operation = None
    columns = []
    if (data[data.find("where"):] != "D"):
        values = str(data[data.find("where"):]).removeprefix("where ")
    elif (data[data.find("on"):] != "D"):
        values = str(data[data.find("on"):]).removeprefix("on ")
    operation = values.split(" ")[1]
    for word in values.split():
        if (len(word) > 1):
            columns.append(word[word.find(".")+1:])
    return [columns, operation]


def get_join_tables(args: str) -> list:
    """
    get the names of tables to preform a join on
    """
    table = []
    fromStatement = args[0].replace("from", "").replace("select", "").replace(
        "inner join", "").replace("left outer join", "").replace(",", "").strip()

    # print(fromStatement)
    for e in fromStatement.split(" "):
        if (len(e) > 1):
            table.append(e)
    return table


def insert_into(data: str) -> None:
    """
    inserts values into table
    """
    tableName = data.split()[0]
    inputData = "|".join(
        data[data.find('(')+1:data.rfind(')')].split(",")).strip()
    table = SamQLTable(activeDB, tableName)
    table.insert_into(inputData)
    del table


def update_tuple(data: str) -> None:
    """
    updates a tables data
    """
    tableName = data.split()[0]
    if (transacting == True):
        if (check_for_lock(tableName) == True):
            print(f"ERROR: Table {tableName} is locked.")
        if (check_for_lock(tableName) == False):
            global transaction_client
            transaction_client = True
            global transaction_table
            transaction_table[0] = tableName
            table = SamQLTable(activeDB, tableName)
            subprocess.run(["cp", table.tablePath, activeDB +
                           "/" + tableName + "_lock"])
            tempTable = SamQLTable(activeDB, tableName +
                                   "_lock", table.columns, isLock=True)
            del table
            tempTable.update_table(data.replace(
                "\n", "").replace(tableName, "").strip())
            return
    else:
        table = SamQLTable(activeDB, tableName)
        table.update_table(data.replace(
            "\n", "").replace(tableName, "").strip())
        del table


def delete_tuple(data: str) -> None:
    """
    deletes data in table
    """
    tableName = data.split()[1].capitalize()
    table = SamQLTable(activeDB, tableName)
    table.delete_from_table(data.replace(
        "\n", "").replace("from product", "").strip())
    del table


def handle_transaction() -> None:
    """
    begins the transaction
    """
    global transacting
    transacting = True
    print("Transaction starts.")


def handle_commit() -> None:
    """
    ends the transaction and converts lock files to table files
    """
    global transacting
    global transaction_client
    if (transaction_client == True):
        subprocess.run(["rm", activeDB + "/"+transaction_table[0]])
        subprocess.run(["mv", activeDB + "/"+transaction_table[0] +
                       "_lock", activeDB + "/"+transaction_table[0]])
        print("Transaction committed.")
    else:
        print("Transaction aborted.")

    transacting = False
    transaction_client = False


def check_for_lock(tableName: str) -> bool:
    """
    checks if the table which is being updated is locked
    """
    if (os.path.exists(activeDB + "/"+tableName+"_lock") == True):
        return True
    else:
        return False


# execute the main function only if the file is run directly
if __name__ == "__main__":
    main()
