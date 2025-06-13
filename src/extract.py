import os
import requests
import json
from datetime import date
import time

google_api_key = os.getenv('GOOGLE_API_KEY')
today = date.today()

def extract_book_data(url, header):
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

        return extract_book_data(url, self.header)


    def fetch_book_data_by_title(self, title, offset=0):
        title = title.replace(' ', '+')
        url = (f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}'
               f'&fields={self.fields}&startIndex={offset}')
        
        return extract_book_data(url, self.header)


    def fetch_book_data_by_genre(self, genre, offset=0):
        genre = genre.replace(' ', '+')
        url = (f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}'
               f'&fields={self.fields}&startIndex={offset}')
        
        return extract_book_data(url, self.header)
    
    def fetch_book_data_by_query(self, query, offset=0):
        url = (f'https://www.googleapis.com/books/v1/volumes?q={query}'
               f'&fields={self.fields}&startIndex={offset}')
        
        return extract_book_data(url, self.header)
        

class OpenLibrary():
    header = {'User-Agent': 'Kalar-LMS nick@kalar.codes'}
    fields = 'author_name,title,isbn'

    def fetch_book_data_by_author(self, author):
        author = author.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?author={author}&lang=en&fields={self.fields}'
        
        return extract_book_data(url, self.header)
        

    def fetch_book_data_by_title(self, title):
        title = title.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?title={title}&lang=en&fields={self.fields}'

        return extract_book_data(url, self.header)


    def fetch_book_data_by_genre(self, genre):
        genre = genre.replace(' ', '+')
        url = f'https://openlibrary.org/search.json?subject={genre}&lang=en&fields={self.fields}'

        return extract_book_data(url, self.header)


def write_open_lib_json(open_lib):
    open_lib_json = json.dumps(open_lib.fetch_book_data_by_title('Pale Blue Dot'), indent=4)
    with open(f'output/open_lib_{today}.json', 'w') as f:
        f.write(open_lib_json)

def write_google_books_json(google_books, query):
    google_books_json = json.dumps(google_books.fetch_book_data_by_query(query), indent=4)
    with open(f'output/google_books_{today}.json', 'a') as f:
        if google_books_json != None:
            f.write(google_books_json) 

def get_google_books_info(google_books, query):
    return google_books.fetch_book_data_by_query(query)

if __name__ == '__main__':
    titles = []
    with open('config/title.txt', 'r') as f:
        for line in f:
            titles.append(line.strip())

    google_books = GoogleBooks()
    open_lib = OpenLibrary()

    google_books_json = {'items':[]}
    open_lib_json = {'items':[]}

    for title in titles:
        open_lib_books = open_lib.fetch_book_data_by_title(title)
        for books in open_lib_books['docs']:
            potential_book = {
                                'author': books['author_name'],
                                'title': books['title'],
                            }

            for isbn in books['isbn']:
                if len(isbn) == 13:
                    query = 'isbn:' + isbn
                    book_info = get_google_books_info(google_books, query)
                    if book_info != {}:

                        potential_book['isbn'] = isbn

                        open_lib_json['items'].append(potential_book)
                        google_books_json['items'].append(book_info['items'][0])

        with open(f'output/google_books_{today}.json', 'a') as f:
            f.write(json.dumps(google_books_json)+',')

        with open(f'output/open_lib_books_{today}.json', 'a') as f:
            f.write(json.dumps(open_lib_json)+',')
        
        print('Title Done')
        time.sleep(5)
        print('Starting Next')
