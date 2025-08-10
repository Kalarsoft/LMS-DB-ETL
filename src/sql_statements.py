collection_item_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "collection_item"(
                        "id" BIGSERIAL PRIMARY KEY,
                        "title" VARCHAR(255) NOT NULL,
                        "author" VARCHAR(255) NOT NULL,
                        "publisher" VARCHAR(255) NOT NULL,
                        "publishing_date" VARCHAR(255) NOT NULL,
                        "loc_number" VARCHAR(255) NULL,
                        "dewey_decimal_number" VARCHAR(255) NULL,
                        "isbn" BIGINT NOT NULL,
                        "sort_title" VARCHAR(255) NOT NULL,
                        "format" VARCHAR(255) NOT NULL,
                        "language" VARCHAR(255) NULL,
                        "page_count" BIGINT NULL,
                        "categories" VARCHAR(255) NULL,
                        "description" VARCHAR(2550) NULL,
                        "price_in_cents" BIGINT NULL,
                        "cover_image_uri" VARCHAR(255) NULL,
                        "is_checked_in" BOOLEAN NOT NULL,
                        "is_archived" BOOLEAN NOT NULL,
                        "is_lost" BOOLEAN NOT NULL,
                        "lost_date" DATE NOT NULL
                    );
                    '''

patron_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "patron"(
                        "id" BIGSERIAL PRIMARY KEY,
                        "name" VARCHAR(255) NOT NULL,
                        "has_good_standing" BOOLEAN NOT NULL,
                        "fee_total" INTEGER NOT NULL,
                        "is_archived" BOOLEAN NOT NULL,
                        "last_login" DATE NOT NULL,
                        "password" VARCHAR(255) NOT NULL
                    );
                    '''

staff_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "staff"(
                        "id" BIGINT NOT NULL,
                        "name" VARCHAR(255) NOT NULL,
                        "password" VARCHAR(255) NOT NULL,
                        "is_archived" BOOLEAN NOT NULL
                    );
                    '''

library_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "library"(
                        "id" BIGINT NOT NULL,
                        "name" VARCHAR(255) NOT NULL,
                        "address" VARCHAR(255) NOT NULL
                    );
                    '''

library_collection_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "library_collection"(
                        "id" BIGINT NOT NULL,
                        "library_id" BIGINT NOT NULL,
                        "item_id" BIGINT NOT NULL
                    );
                    '''

lost_item_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "lost_item"(
                        "id" BIGSERIAL PRIMARY KEY,
                        "item_id" BIGINT NOT NULL,
                        "patron_id" BIGINT NOT NULL,
                        "due_date" DATE NOT NULL,
                        "cost_in_cents" INTEGER NOT NULL
                    );
                    ALTER TABLE
                        "lost_item" ADD CONSTRAINT "lost_item_item_id_unique" UNIQUE("item_id");
                    '''

late_item_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "late_item"(
                        "id" BIGSERIAL PRIMARY KEY,
                        "item_id" BIGINT NOT NULL,
                        "patron_id" BIGINT NOT NULL,
                        "due_date" DATE NOT NULL,
                        "fees_in_cents" INTEGER NOT NULL
                    );
                    ALTER TABLE
                        "late_item" ADD CONSTRAINT "late_item_item_id_unique" UNIQUE("item_id");
                    '''

checked_out_item_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "checked_out_item"(
                        "id" BIGINT NOT NULL,
                        "item_id" BIGINT NOT NULL,
                        "patron_id" BIGINT NOT NULL,
                        "due_date" DATE NOT NULL
                    );
                    ALTER TABLE
                        "checked_out_item" ADD CONSTRAINT "checked_out_item_item_id_unique" UNIQUE("item_id");
                    '''

# Does not include the constrant on item_id (like the above) as the same book can be on hold for multiple patrons
# This might need to be changed to item_title instead of item_id since libraries can have multiple copies
on_hold_item_table_creation = '''
                    CREATE TABLE IF NOT EXISTS "on_hold_item"(
                        "id" BIGINT NOT NULL,
                        "item_id" BIGINT NOT NULL,
                        "patron_id" BIGINT NOT NULL,
                        "is_current_hold" BOOLEAN NOT NULL,
                        "hold_release_date" DATE NOT NULL
                    );
                    '''

# To be ran after all the above
foreign_key_creation = '''
                    ALTER TABLE
                        "lost_item" ADD CONSTRAINT "lost_item_item_id_foreign" FOREIGN KEY("item_id") REFERENCES "collection_item"("id");
                    ALTER TABLE
                        "late_item" ADD CONSTRAINT "late_item_item_id_foreign" FOREIGN KEY("item_id") REFERENCES "collection_item"("id");
                    ALTER TABLE
                        "checked_out_item" ADD CONSTRAINT "checked_out_item_patron_id_foreign" FOREIGN KEY("patron_id") REFERENCES "patron"("id");
                    ALTER TABLE
                        "checked_out_item" ADD CONSTRAINT "checked_out_item_item_id_foreign" FOREIGN KEY("item_id") REFERENCES "collection_item"("id");
                    ALTER TABLE
                        "late_item" ADD CONSTRAINT "late_item_patron_id_foreign" FOREIGN KEY("patron_id") REFERENCES "patron"("id");
                    ALTER TABLE
                        "library_collection" ADD CONSTRAINT "library_collection_library_foreign" FOREIGN KEY("library_id") REFERENCES "library"("id");
                    ALTER TABLE
                        "lost_item" ADD CONSTRAINT "lost_item_patron_id_foreign" FOREIGN KEY("patron_id") REFERENCES "patron"("id");
                    ALTER TABLE
                        "library_collection" ADD CONSTRAINT "library_collection_item_foreign" FOREIGN KEY("item_id") REFERENCES "collection_item"("id");
                    ALTER TABLE
                        "on_hold_item" ADD CONSTRAINT "on_hold_item_patron_id_foreign" FOREIGN KEY("patron_id") REFERENCES "patron"("id");
                    ALTER TABLE
                        "on_hold_item" ADD CONSTRAINT "on_hold_item_item_id_foreign" FOREIGN KEY("item_id") REFERENCES "collection_item"("id");
                    '''

def collection_insert_statement(book):
    return ('INSERT INTO Collection_Item ' 
    '(title, author, publisher, publishing_date, loc_number, dewey_decimal_number, isbn, sort_title, format, '
    'language, categories, page_count, description, price_in_cents, is_checked_in, is_archived, is_lost, lost_date) '
    f'VALUES (\'{book['title']}\', \'{book['author']}\', '
    f'\'{book['publisher']}\', \'{book['publishing_date']}\', '
    f'\'{book['loc_number']}\', \'{book['dewey_decimal_number']}\', '
    f'\'{book['isbn']}\', \'{book['sort_title']}\',' 
    f'\'{book['format']}\', \'{book['language']}\', '
    f'\'{book['categories']}\', \'{book['page_count']}\', '
    f'\'{book['description']}\', \'{book['price_in_cents']}\', '
    f'\'{book['is_checked_in']}\', \'{book['is_archived']}\', '
    f'\'{book['is_lost']}\', \'{book['lost_date']}\');')