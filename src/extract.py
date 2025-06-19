import os
import time
import logging
import requests
import json
from dotenv import load_dotenv
from datetime import date, datetime


load_dotenv

google_api_key = os.getenv('GOOGLE_API_KEY')
google_header = {'key': google_api_key}
open_lib_header = {'User-Agent': 'Kalar-LMS nick@kalar.codes'}

logger = logging.getLogger('extract.py')
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=os.getenv('LOGGING_LEVEL'))

today = date.today()

def extract_book_json(url, header=[]):
    '''
        Returns a dictionary (JSON) of books or an empty dictionary on error.

        Keyword arguments:
        url    -- the url used to make the request.
        header -- the optional headers passed to specify things needed for the queries, like API keys.
    '''
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(f'An error occurred: {err}')
        return {}
    return response.json()

def get_google_book_data(query, offset=0):
    '''
        Returns a dictionary of books from the Google Books API based on a query.

        Keyword arguments:
        query  -- a string used to find a list of books by a specific attribute provided by 
                  the Google Books API.
        offset -- the optional page offset for a query. Google Books API limits the number 
                  of responses per query and returns an ordered list. This allows you to skip 
                  the first x number of responses.
    '''
    query = query.replace(' ', '+')
    fields = ('items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate,'
            'volumeInfo/publisher,volumeInfo/categories,volumeInfo/pageCount,'
            'volumeInfo/language,volumeInfo/printType,volumeInfo/description)')
    url = (f'https://www.googleapis.com/books/v1/volumes?q={query}'
            f'&fields={fields}&startIndex={offset}')
    return extract_book_json(url, google_header)

def get_open_library_book_data(query, offset=0):
    '''
        Returns a dictionary of books from the Open Library API based on a query.

        Keyword arguments:
        query  -- a string used to find a list of books by a specific attribute provided by 
                  the Open Library API.
        offset -- the optional page offset for a query. The Open Library API limits the number 
                  of responses per query and returns an ordered list. This allows you to skip 
                  the first x number of responses.
    '''
    query = query.replace(' ', '+')
    fields = 'author_name,title,isbn'
    url = f'https://openlibrary.org/search.json?{query}&lang=en&fields={fields}&offset={offset}'

    return extract_book_json(url, open_lib_header)


def start():
    titles = []
    google_books_array = []
    open_lib_array = []
    with open('config/title.txt', 'r') as google_books_file:
        for line in google_books_file:
            titles.append(line.strip())

    with open(f'output/raw_google_books_{today}.json', 'w') as google_books_file, \
         open(f'output/raw_open_lib_books_{today}.json', 'w') as open_lib_file:
        google_books_file.write('{"book_data":')
        open_lib_file.write('{"book_data":')
    
        for title in titles:
            open_lib_query = f'title={title}'
            open_lib_books = get_open_library_book_data(open_lib_query)
            for books in open_lib_books['docs']:
                logger.info(f'{datetime.now()}:Book found: {str(books)}')
                if 'author_name' in books \
                and 'title' in books \
                and 'isbn' in books:
                    for isbn in books['isbn']:
                        if len(isbn) == 13:
                            google_query = 'isbn:' + isbn
                            google_book_info = get_google_book_data(google_query)

                            if google_book_info != {}:
                                potential_ol_book = books
                                potential_ol_book['isbn'] = isbn

                                open_lib_array.append(potential_ol_book)
                                google_books_array.append(google_book_info['items'][0])
                            time.sleep(.5)
            time.sleep(.5)

        google_books_file.write(json.dumps(google_books_array)+'}')
        open_lib_file.write(json.dumps(open_lib_array)+'}')
    

if __name__ == '__main__':
    print('Extraction Started')
    logger.info(f'{datetime.now()}:Extraction Started')
    start()
    print('Extraction Done')
    logger.info(f'{datetime.now()}:Extraction Done')
