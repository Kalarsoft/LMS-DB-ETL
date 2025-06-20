import os
import logging
import json
import psycopg
from dotenv import load_dotenv
from datetime import date, datetime

load_dotenv()

logger = logging.getLogger('load.py')
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=logging.INFO)

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

today = date.today()

collections_table_creation = '''
                    CREATE TABLE IF NOT EXISTS Collection_Item(
                        "id" BIGSERIAL PRIMARY KEY,
                        "title" VARCHAR(255) NULL,
                        "author" VARCHAR(255) NULL,
                        "publisher" VARCHAR(255) NULL,
                        "publishing_date" VARCHAR(255) NULL,
                        "loc_number" VARCHAR(255) NULL,
                        "dewey_decimal_number" VARCHAR(255) NULL,
                        "isbn" BIGINT NULL,
                        "sort_title" VARCHAR(255) NULL,
                        "format" VARCHAR(255) NULL,
                        "language" VARCHAR(255) NULL,
                        "page_count" BIGINT NULL,
                        "categories" VARCHAR(255) NULL,
                        "description" BIGINT NULL,
                        "price_in_cents" BIGINT NULL,
                        "cover_image_uri" VARCHAR(255) NULL,
                        "is_checked_in" BOOLEAN NULL,
                        "is_archived" BOOLEAN NULL,
                        "is_lost" BOOLEAN NULL,
                        "lost_date" DATE NULL
                    )
                    '''

def start():
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password}') as conn, \
        open(f'output/transformed_{today}.json', 'r') as transformed_books:
        with conn.cursor() as cur:
            cur.execute(f'DROP TABLE IF EXISTS Collection_Item') # TODO: REMOVE WHEN TESTING COMPLETED
            cur.execute(collections_table_creation)
            books = json.loads(transformed_books.read())

            for book in books['books']:
                cur.execute(f'INSERT INTO Collection_Item ' \
                            '(title, author, publisher, publishing_date, isbn, sort_title, format, language, categories, page_count, is_checked_in, is_archived, is_lost) ' \
                            f'VALUES (\'{book['title']}\',\'{book['author']}\',\'{book['publisher']}\',\'{book['publishing_date']}\',{book['isbn']},\'{book['sort_title']}\','
                            f'\'{book['format']}\',\'{book['language']}\',\'{book['categories']}\',{book['page_count']},{book['is_checked_in']},{book['is_archived']},{book['is_lost']});')
                logger.info(f'{datetime.now()}:Book {book['title']} loaded.')

def load_transformed_books():
    pass

if __name__ == '__main__':
    print('Loading Started')
    logger.info(f'{datetime.now()}:Loading Started')
    start()
    print('Loading Done')
    logger.info(f'{datetime.now()}:Loading Done')
