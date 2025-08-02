


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


def collection_insert_statement(book):
    return 'INSERT INTO Collection_Item ' \
    '(title, author, publisher, publishing_date, isbn, sort_title, format, '\
    'language, categories, page_count, is_checked_in, is_archived, is_lost) '\
    f'VALUES (\'{book['title']}\', \'{book['author']}\', '\
    f'\'{book['publisher']}\', \'{book['publishing_date']}\', '\
    f'\'{book['isbn']}\', \'{book['sort_title']}\',' \
    f'\'{book['format']}\', \'{book['language']}\', '\
    f'\'{book['categories']}\', \'{book['page_count']}\', '\
    f'\'{book['is_checked_in']}\', \'{book['is_archived']}\', '\
    f'\'{book['is_lost']}\');'