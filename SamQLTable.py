import os
import subprocess


class SamQLTable:
    """
    class for the table
    """

    def __init__(self, activeDB: str, tableName: str, attributes: str = None, isLock=False):
        """
        table class constructor
        """
        self.activeDB = activeDB
        self.tableName = tableName
        self.tablePath = f"{activeDB}/{tableName}"
        if (attributes != None):
            self.create_table(attributes, isLock)
            self.__init__(self.activeDB, self.tableName)
        else:
            self.tableContents = self.read_table_file(self.tablePath)
            self.columns = self.tableContents[0]
            self.numOfCols = len(self.columns.split("|"))
            self.rows = self.tableContents[1:]
            self.numOfRows = len(self.rows)

    def create_table(self, columns: str, isLock: bool) -> None:
        """
        creates a table with columns specified
        input: string columns
        output: confirmation or error
        return: none
        """
        if (os.path.exists(self.tablePath) == False):
            input = "".join(columns).replace(", ", "|").strip()
            subprocess.run(["touch", f"{self.tablePath}"])
            with open(self.tablePath, "w", newline='') as file:
                file.write(input)
                file.close()
            if (isLock == False):
                print(f"Created table {self.tableName}")
        else:
            if (isLock == True):
                return
            else:
                print(f"ERROR: Table {self.tableName} exists")

    def read_table_file(self, tablePath: str) -> list:
        """
        reads the contents of a table and returns it as a list
        input: table path
        output: none
        return: table contents in a list
        """
        tableContents = []
        with open(tablePath, "r") as file:
            fileContents = file.readlines()
            for line in fileContents:
                tableContents.append(line.strip())
            file.close()
        return tableContents

    def refresh_table(self) -> None:
        """
        refreshes table contents with updated columns
        and rows
        input: none
        output: none
        return: none
        """
        self.tableContents.clear()
        self.tableContents.append(self.columns)
        for i in range(0, self.numOfRows):
            self.tableContents.append(self.rows[i])
        self.update_table_file()

    def update_table_file(self) -> None:
        """
        updates the table file
        input: non
        output: none
        return: none
        """
        with open(self.tablePath, "w") as file:
            for row in self.tableContents:
                file.write(row.strip() + "\n")
            file.close()

    def print_table(self) -> None:
        """
        prints the contents of a table
        input: none
        output: table contents in console
        return: none
        """
        for line in self.tableContents:
            print(line.replace("|", " | "))

    def insert_into(self, input: str) -> None:
        """
        inserts data into a table
        input: string of values to input
        ex: "1,'Gizmo',19.99"
        output: records inserted
        return: none
        """
        if (os.path.exists(self.tablePath) == True):
            recsInserted = 0
            inputData = input.replace(
                ",", "|").replace("'", "").split()[0]
            with open(self.tablePath, "a") as file:
                file.write(inputData)
                file.close()
            recsInserted += 1
            self.numOfRows += 1
            self.rows.append(inputData)
            self.refresh_table()
            print(f"{recsInserted} record(s) inserted.")
        else:
            print(f"ERROR: Table {self.tableName} does not exist.")

    def alter_table(self, attribute: str) -> None:
        """
        alters the columns of a table
        input: string new attribute
        output: confirmation or error
        return: none
        """
        if (os.path.exists(self.tablePath) == True):
            self.columns = f"{self.columns}{attribute}"
            self.numOfCols += 1
            self.refresh_table()
            print(f"Table {self.tableName} modified.")
        else:
            print(f"ERROR: Table {self.tableName} does not exist.")

    def update_table(self, args: str) -> None:
        """
        updates a table where specified
        input: string of arguments
        output: records modified
        return: none
        """
        recsModified = 0
        # get set conditions
        sColumn, sOpertaion, sNewValue = args.split(
        )[args.split().index("set")+1:(args.split().index("set")+1)+self.numOfCols+2]
        sColumnIndex = self.get_column_index(sColumn)
        # get where conditions
        wColumn, wOpertaion, wOldValue = args.split(
        )[args.split().index("where")+1:(args.split().index("where")+1)+self.numOfCols+2]
        wColumnIndex = self.get_column_index(wColumn)

        newRow = []
        for row in self.rows:
            if (wOpertaion == "="):
                if (row.split("|")[wColumnIndex].replace("'", "") == wOldValue.replace("'", "")):
                    oldRow = row
                    newRow = row.split("|")
                    newRow[sColumnIndex] = clean_string(sNewValue)
                    self.rows[self.rows.index(oldRow)] = "|".join(newRow)
                    recsModified += 1
        print(f"{recsModified} records modified.")
        self.refresh_table()

    def delete_from_table(self, args: str) -> None:
        """
        deletes a entry from table depending on condition
        input: statement with the condition
        output: records deleted
        return: none
        """
        column, operation, value = args.replace("'", "").split()[0:]
        columnIndex = self.get_column_index(column)
        recsDeleted = 0

        if (operation == "="):
            for row in self.rows:
                if (value in row.split("|")):
                    self.rows.remove(row)
                    self.numOfRows -= 1
                    recsDeleted += 1
                    self.refresh_table()
        elif (operation == ">"):
            for row in self.rows:
                try:
                    if (float(row.split("|")[columnIndex]) > float(value)):
                        self.rows.remove(row)
                        self.numOfRows -= 1
                        recsDeleted += 1
                        self.refresh_table()
                except:
                    TypeError
                    print(f"ERROR: {value} is not a number.")
                    break
        print(f"{recsDeleted} records deleted.")

    def select_from_table(self, args: str) -> str:
        """
        selects certain rows based on a condition 
        sends to external function to print
        input: string of arguments
        output: none
        return: none
        """
        result = []

        selectors = args.replace(",", "").split()[args.split().index(
            "select")+1:args.split().index("from")]

        selectorIndicies = []
        for selector in selectors:
            for i in range(0, self.numOfCols):
                if (selector in self.columns.split("|")[i]):
                    selectorIndicies.append(i)

        for row in self.tableContents:
            for e in row.split("|"):
                if row.split("|").index(e) in selectorIndicies:
                    result.append(e.strip())
        print("RESULT:",result)
        # print_list_formatted(result, len(selectorIndicies))
        return result

    def drop_table(self) -> None:
        """
        deletes a table
        input: none
        output: confirmation or error
        return: none
        """
        if (os.path.exists(self.tablePath) == True):
            subprocess.run(["rm", f"{self.tablePath}"])
            print(f"Dropped table {self.tableName}.")
        else:
            print(f"ERROR: {self.tableName} does not exist.")

    def get_column_index(self, column: str) -> int:
        """
        gets the index of a attribute from the columns list
        input: string the column
        output: none
        return: int the index
        """
        columnIndex = 0
        for columns in self.columns.split("|"):
            if (column in columns.split()):
                columnIndex = self.columns.split("|").index(columns)
        return columnIndex


# utility functions
def clean_string(string: str) -> str:
    """
    removes single quotes from strings 
    input: string columns
    output: none
    return: string without single quotes
    """
    return string.replace("'", "")


def print_list_formatted(table: list, tableWidth: int) -> None:
    """
    prints a list in the table format based on its width
    input: list table int width of the table 
    output: list in table format 
    return: none
    """
    print("PRINT LIST FORMATTED:",table)
    for i in range(0, tableWidth+4, tableWidth):
        print("".join(table[i] +
                      " | " + "".join(table[i+1])))
