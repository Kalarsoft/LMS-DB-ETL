import os
from dotenv import load_dotenv
import psycopg
from datetime import date

load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

today = date.today()

collections_table_creation = """
                    CREATE TABLE IF NOT EXISTS "Collection_Item"(
                        "id" BIGINT PRIMARY KEY,
                        "title" VARCHAR(255) NULL,
                        "author" VARCHAR(255) NULL,
                        "publisher" VARCHAR(255) NULL,
                        "publishing_date" DATE NULL,
                        "loc_number" VARCHAR(255) NULL,
                        "dewey_decimal_number" VARCHAR(255) NULL,
                        "sort_title" VARCHAR(255) NULL,
                        "format" VARCHAR(255) NULL,
                        "language" VARCHAR(255) NULL,
                        "page_count" BIGINT NULL,
                        "genre" VARCHAR(255) NULL,
                        "subject" VARCHAR(255) NULL,
                        "description" BIGINT NULL,
                        "price_in_cents" BIGINT NULL,
                        "cover_image_uri" VARCHAR(255) NULL,
                        "is_checked_in" BOOLEAN NULL,
                        "is_archived" BOOLEAN NULL,
                        "is_lost" BOOLEAN NULL,
                        "lost_date" DATE NULL
                    )
                    """

def start():
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password}') as conn, \
        open(f"output/transformed_{today}", 'r'):
        with conn.cursor() as cur:
            cur.execute(collections_table_creation)


def load_transformed_books():
    pass

if __name__ == '__main__':
    start()