import os
import logging
import json
import psycopg
from dotenv import load_dotenv
from datetime import date, datetime
import sql_statements

load_dotenv()

logger = logging.getLogger('load.py')
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=logging.INFO)

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

today = date.today()

collections_table_creation = sql_statements.collections_table_creation

def start():
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password}') as conn, \
        open(f'output/transformed_{today}.json', 'r') as transformed_books:
        with conn.cursor() as cur:
            cur.execute(f'DROP TABLE IF EXISTS Collection_Item') # TODO: REMOVE WHEN TESTING COMPLETED
            cur.execute(collections_table_creation)
            books = json.loads(transformed_books.read())

            for book in books['books']:
                cur.execute(sql_statements.collection_insert_statement(book))
                logger.info(f'{datetime.now()}:Book {book['title']} loaded.')

def load_transformed_books():
    pass

if __name__ == '__main__':
    print('Loading Started')
    logger.info(f'{datetime.now()}:Loading Started')
    start()
    print('Loading Done')
    logger.info(f'{datetime.now()}:Loading Done')
