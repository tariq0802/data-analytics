from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import errorcode
from cdata.items import CdataItem
import logging


class CdataPipeline:

    def __init__(self):
        self.conn = self.create_connection()
        self.create_batters_table()
        self.create_bowlers_table()
        self.create_links_table()
        self.create_playing_table()

    def create_connection(self):
        try:
            conn = mysql.connector.connect(
                user="root",
                password="Dachduna0",
                host="localhost",
                database="cricket",
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

    def create_links_table(self):
        cursor = self.conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS links (
            id INT AUTO_INCREMENT PRIMARY KEY,
            link VARCHAR(255) NOT NULL UNIQUE
        )
        """
        logging.info(f"Executing query: {create_table_query}")
        cursor.execute(create_table_query)
        self.conn.commit()

    def create_batters_table(self):
        cursor = self.conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS batters (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Date DATE,
            Name VARCHAR(255),
            Team VARCHAR(255),
            Runs INT,
            Balls INT,
            4s INT,
            6s INT,
            SR FLOAT,
            Game VARCHAR(255),
            Series VARCHAR(255),
            Venue VARCHAR(255)           
        )
        """
        logging.info(f"Executing query: {create_table_query}")
        cursor.execute(create_table_query)
        self.conn.commit()

    def create_bowlers_table(self):
        cursor = self.conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS bowlers (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Date DATE,
            Name VARCHAR(255),
            Team VARCHAR(255),
            Overs FLOAT,
            Maiden INT,
            Given INT,
            Wicket INT,
            Economy FLOAT,
            WB INT,
            NB INT,
            Game VARCHAR(255),
            Series VARCHAR(255),
            Venue VARCHAR(255)
        )
        """
        logging.info(f"Executing query: {create_table_query}")
        cursor.execute(create_table_query)
        self.conn.commit()

    def create_playing_table(self):
        cursor = self.conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS playing (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Game VARCHAR(255),
            Name VARCHAR(255)
        )
        """
        logging.info(f"Executing query: {create_table_query}")
        cursor.execute(create_table_query)
        self.conn.commit()

    def link_exists_in_database(self, link):
        cursor = self.conn.cursor()
        query = "SELECT * FROM links WHERE link = %s"
        cursor.execute(query, (link,))
        return cursor.fetchone() is not None

    def save_link_to_database(self, link):
        cursor = self.conn.cursor()
        query = "INSERT INTO links (link) VALUES (%s)"
        cursor.execute(query, (link,))
        self.conn.commit()

    def process_batter_item(self, item):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO batters (Date, Team, Name, Runs, Balls, 4s, 6s, SR, Game, Series, Venue)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                item["date"],
                item["team"],
                item["name"],
                item["run"],
                item["ball"],
                item["four"],
                item["six"],
                item["sr"],
                item["match_no"],
                item["series"],
                item["venue"],
            ),
        )
        self.conn.commit()

    def process_bowler_item(self, item):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO bowlers (Date, Team, Name, Overs, Maiden, Given, Wicket, Economy, WB, NB, Game, Series, Venue)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                item["date"],
                item["bowling_team"],
                item["bowler"],
                item["over"],
                item["maiden"],
                item["given"],
                item["wicket"],
                item["eco"],
                item["wide"],
                item["nb"],
                item["match_no"],
                item["series"],
                item["venue"],
            ),
        )
        self.conn.commit()

    def process_playing_item(self, item):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO playing (Game, Name)
            VALUES (%s, %s)
            """,
            (
                item["play_no"],
                item["player"],
            ),
        )
        self.conn.commit()

    def process_item(self, item, spider):
        if "run" in item:
            self.process_batter_item(item)
        elif "over" in item:
            self.process_bowler_item(item)
        elif "player" in item:
            self.process_playing_item(item)
        else:
            pass
        return item

    def close_spider(self, spider):
        self.conn.close()
