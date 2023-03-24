import sqlite3
import datetime

from log import log


class DBHelper:
    def __init__(self):
        self.db_path='config/test.db'
        self.conn = sqlite3.connect(self.db_path)
        self.try_create_table()

    def try_create_table(self):
        create_posts_table = """
        CREATE TABLE IF NOT EXISTS connections(
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          conn_id TEXT NOT NULL,
          raw_insert_date TEXT NOT NULL,
          network TEXT NOT NULL,
          type TEXT NOT NULL,
          source_ip TEXT NOT NULL,
          source_port TEXT NOT NULL,
          dest_ip TEXT NOT NULL,
          dest_port TEXT NOT NULL,
          host TEXT,
          upload INT NOT NULL,
          download INT NOT NULL,
          start CHAR(50),
          rule TEXT,
          chains TEXT,
          proxy TEXT NOT NULL
        );
        """
        self.execute_query(create_posts_table)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully")
        except Exception as e:
            log(f"The error '{e}' occurred")

    def insert(self, connection):
        connect_id = connection["id"]
        cur_time = datetime.datetime.utcnow().isoformat()
        # metadata is object
        metadata = connection['metadata']
        # chains is array
        chains = connection['chains']
        chains_str = ""
        for chain in chains:
            chains_str = "/"+chains_str if chains_str else ""
            chains_str = chain + chains_str

        create_connect = f"""
        INSERT INTO
          connections (conn_id, raw_insert_date, network, type, source_ip, source_port, dest_ip, dest_port, host, upload, download, start, rule, chains, proxy)
        VALUES(
          "{connect_id}", 
          "{cur_time}",
          "{metadata['network']}", 
          "{metadata['type']}", 
          "{metadata['sourceIP']}",
          "{metadata['sourcePort']}",
          "{metadata['destinationIP']}",
          "{metadata['destinationPort']}",
          "{metadata['host']}",
          "{connection['upload']}",
          "{connection['download']}",
          "{connection['start']}",
          "{connection['rule']}",
          "{chains_str}",
          "{chains[0]}"
        );
        """

        print('insert: %s ' % connect_id)
        self.execute_query(create_connect)

    def close_db(self):
        self.conn.close()

    def parse_res_value(self, sql):
        res = self.fetch_data(sql)
        category = []
        value = []

        for index, item in enumerate(res):
            category.append(item[0])
            value.append(item[1])

        category.reverse()
        value.reverse()

        res_json = {
                "category": category,
                "value": value
        }

        return res_json

    def fetch_data(self, query):
        cursor = self.conn.cursor()
        try:
            res = cursor.execute(query)
            print("Query executed successfully")
            return res.fetchall()
        except Exception as e:
            log(f"The error '{e}' occurred")


if __name__ == "__main__":
    pass
    # db_helper = DBHelper()
    # message = json.loads(test_message_json)
    # db_helper.insert(
    #     message['connections'][0]
    # )
