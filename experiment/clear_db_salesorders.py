import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

if __name__ == '__main__':
    connection = create_connection("db.sqlite3")
    if connection:
        cursor = connection.cursor()

        # Need to delete the line items first due to foreign key
        del_items = "DELETE FROM sale_unleashedsalesorder_line_item"
        cursor.execute(del_items)
        print(cursor.rowcount, " rows have been deleted from sale_unleashedsalesorder_line_item")

        # Next delete the sales orders
        del_items = "DELETE FROM sale_unleashedsalesorder"
        cursor.execute(del_items)
        print(cursor.rowcount, " rows have been deleted from sale_unleashedsalesorder")

        connection.commit()
        connection.close()
    else:
        print("Failed to open a connection to the database")