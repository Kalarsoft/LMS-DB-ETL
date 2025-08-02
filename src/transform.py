import os
import json
import logging
from datetime import date, datetime

logger = logging.getLogger('transform.py')
logging.basicConfig(filename=os.getenv('LOG_FILE'), level=logging.INFO)

today = date.today()

def get_raw_json(path):
    '''
        Returns a dictionary read from a JSON file.

        Keyword arguments:
        path - the relative path for the JSON file to be read.
    '''
    with open(path, 'r') as json_file:
        return json.loads(json_file.read())
    
def format_sort_title(title):
    '''
        Returns a string with any leading article moved to the end.

        Keyword arguments:
        title - the string to be formatted.
    '''
    if title.lower().startswith('the '):
        return f'{title[4:]}, {title[0:3]}'
    elif title.lower().startswith('a '):
        return f'{title[2:]}, {title[0]}'
    elif title.lower().startswith('an '):
        return f'{title[3:]}, {title[0:2]}'
    return title
        
def combine_raw_jsons(google_json, ol_json):
    '''
        Returns a dictionary consisting of an array of dictionarys. 
        Each child dictionary is a transformed book ready to be 
        inserted into a database.

        Keyword arguments:
        google_json - A dictionary consisting of raw data from the Google Books API
        ol_json - A dictionary consisting of raw data from the OpenLibrary API
    '''
    transformed_dictionary = {'books': []}
    for index in range(len(google_json['book_data'])):
        transformed_dictionary_entry = {}
        replace_quote = str.maketrans({"'": r"_"})
        
        title = str(google_json['book_data'][index]['volumeInfo']['title']).translate(replace_quote)
        author = ', '.join(ol_json['book_data'][index]['author_name']).translate(replace_quote)
        isbn = ol_json['book_data'][index]['isbn']
        sort_title = format_sort_title(title)

        if 'categories' in google_json['book_data'][index]['volumeInfo']:
            categories = ', '.join(google_json['book_data'][index]['volumeInfo']['categories'])
        else:
            categories = None
        
        if 'publisher' in google_json['book_data'][index]['volumeInfo']:
            publisher = str(google_json['book_data'][index]['volumeInfo']['publisher']).translate(replace_quote)
        else:
            publisher = None

        if 'publishedDate' in google_json['book_data'][index]['volumeInfo']:
            published_date = google_json['book_data'][index]['volumeInfo']['publishedDate']
        else:
            published_date = None

        if 'printType' in google_json['book_data'][index]['volumeInfo']:
            print_type = google_json['book_data'][index]['volumeInfo']['printType']
        else:
            print_type = None

        if 'language' in google_json['book_data'][index]['volumeInfo']:
            language = google_json['book_data'][index]['volumeInfo']['language']
        else:
            language = None

        if 'pageCount' in google_json['book_data'][index]['volumeInfo']:
            pageCount = google_json['book_data'][index]['volumeInfo']['pageCount']
        else:
            pageCount = 0
        
        transformed_dictionary_entry = {
            'title':           title,
            'author':          author,
            'publisher':       publisher,
            'publishing_date': published_date,
            'isbn':            isbn,
            'sort_title':      sort_title,
            'format':          print_type,
            'language':        language,
            'categories':      categories,
            'page_count':      pageCount,
            'is_checked_in':   True,
            'is_archived':     False,
            'is_lost':         False,
        }
        transformed_dictionary['books'].append(transformed_dictionary_entry)

    return transformed_dictionary

def start():
    google_json = get_raw_json(f'output/raw_google_books_{today}.json')
    ol_json = get_raw_json(f'output/raw_open_lib_books_{today}.json')
    with open(f'output/transformed_{today}.json', 'w') as transformed:
        transformed.write(json.dumps(combine_raw_jsons(google_json, ol_json)))

if __name__ == '__main__':
    print('Transformation Started')
    logger.info(f'{datetime.now()}:Transformation Started')
    start()
    print('Transformation Done')
    logger.info(f'{datetime.now()}:Transformation Done')
