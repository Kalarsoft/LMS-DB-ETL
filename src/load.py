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

def start():
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password}') as conn, \
        open(f'output/transformed_{today}.json', 'r') as transformed_books:
            books = json.loads(transformed_books.read())
            with conn.cursor() as cur:
                cur.execute(f'DROP TABLE IF EXISTS Collection_Item') # TODO: REMOVE WHEN TESTING COMPLETED
                cur.execute(sql_statements.collections_table_creation)
                load_transformed_books(cur, books)
            

def load_transformed_books(cursor, books):
    '''
        Takes a pyscopg connection cursor and a dictionary of books and inserts
        the books into a PostgreSQL database.

        Keyword arguments:
        cursor - a psycopg.connect.cursor object
        books  - a dictionary of transformed books following the schema for the 
                 `collection_item` SQL table
    '''
    for book in books['books']:
        cursor.execute(sql_statements.collection_insert_statement(book))
        logger.info(f'{datetime.now()}:Book {book['title']} loaded.')

if __name__ == '__main__':
    print('Loading Started')
    logger.info(f'{datetime.now()}:Loading Started')
    start()
    print('Loading Done')
    logger.info(f'{datetime.now()}:Loading Done')
