from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import errorcode


class PslPipeline:
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = mysql.connector.connect(
                user="root",
                password="Dachduna0",
                host="localhost",
                database="psl",
            )
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Access denied.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            else:
                print(f"Error: {err}")
            raise

    def process_item(self, item, spider):
        return item
