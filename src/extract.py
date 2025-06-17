import os
from dotenv import load_dotenv
import requests
import json
from datetime import date
import time

load_dotenv

google_api_key = os.getenv('GOOGLE_API_KEY')
today = date.today()

def extract_book_json(url, header):
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemError(err)
    return response.json()

class GoogleBooks():
    header = {'key': google_api_key}
    fields = "items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate," \
    "volumeInfo/publisher,volumeInfo/categories,volumeInfo/pageCount,volumeInfo/printType)"

    def fetch_book_data_by_author(self, author, offset=0):
        author = author.replace(' ', '+')
        url = (f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}'
               f'&fields={self.fields}&startIndex={offset}')

        return extract_book_json(url, self.header)


    def fetch_book_data_by_title(self, title, offset=0):
        title = title.replace(' ', '+')
        url = (f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}'
               f'&fields={self.fields}&startIndex={offset}')
        
        return extract_book_json(url, self.header)


    def fetch_book_data_by_genre(self, genre, offset=0):
        genre = genre.replace(' ', '+')
        url = (f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}'
               f'&fields={self.fields}&startIndex={offset}')
        
        return extract_book_json(url, self.header)
    
    def fetch_book_data_by_query(self, query, offset=0):
        url = (f'https://www.googleapis.com/books/v1/volumes?q={query}'
               f'&fields={self.fields}&startIndex={offset}')
        
        return extract_book_json(url, self.header)
        

class OpenLibrary():
    header = {'User-Agent': 'Kalar-LMS nick@kalar.codes'}
    fields = 'author_name,title,isbn'

    def fetch_book_data_by_author(self, author):
        author = author.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?author={author}&lang=en&fields={self.fields}'
        
        return extract_book_json(url, self.header)

    def fetch_book_data_by_title(self, title):
        title = title.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?title={title}&lang=en&fields={self.fields}'

        return extract_book_json(url, self.header)

    def fetch_book_data_by_genre(self, genre):
        genre = genre.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?subject={genre}&lang=en&fields={self.fields}'

        return extract_book_json(url, self.header)


def start():
    titles = []
    with open('config/title.txt', 'r') as google_books_file:
        for line in google_books_file:
            titles.append(line.strip())

    google_books = GoogleBooks()
    open_lib = OpenLibrary()

    google_books_array = []
    open_lib_array = []

    with open(f'output/raw_google_books_{today}.json', 'w') as google_books_file, \
         open(f'output/raw_open_lib_books_{today}.json', 'w') as open_lib_file:
        google_books_file.write('{"book_data":')
        open_lib_file.write('{"book_data":')
    
        for title in titles:
            open_lib_books = open_lib.fetch_book_data_by_title(title)
            for books in open_lib_books['docs']:
                print(str(books))
                if 'author_name' in books \
                and 'title' in books \
                and 'isbn' in books:
                    for isbn in books['isbn']:
                        if len(isbn) == 13:
                            query = 'isbn:' + isbn
                            google_book_info = google_books.fetch_book_data_by_query(query)

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
    start()
