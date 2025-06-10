import os
import requests
import json

google_api_key = os.getenv("GOOGLE_API_KEY")

class GoogleBooks():
    def fetch_book_data_by_author(author, offset=0):
        url = (f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
               "&fields=items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate,"
               f"volumeInfo/industryIdentifiers,volumeInfo/categories)&startIndex={offset}")

        response = requests.get(url, headers={"key": google_api_key})
        return response.json()


    def fetch_book_data_by_title(title, offset=0):
        title = title.replace(" ", "+")

        url = (f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
               "&fields=items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate,"
               f"volumeInfo/industryIdentifiers,volumeInfo/categories)&startIndex={offset}")
        
        response = requests.get(url, headers={'key': google_api_key})
        return response.json()

    def fetch_book_data_by_genre(genre, offset=0):
        pass

class OpenLibrary():
    def fetch_book_data_by_author(author):
        url = f"https://openlibrary.org/search.json?author={author}&lang=en&fields=author_name,title,key,isbn"
        
        response = requests.get(url, headers={'User-Agent': 'Kalar-LMS nick@kalar.codes'})
        return response.json()

    def fetch_book_data_by_title(title):
        pass

    def fetch_book_data_by_genre(genre):
        pass

if __name__ == "__main__":
    print(GoogleBooks.fetch_book_data_by_author('Tolkien'))
    print(OpenLibrary.fetch_book_data_by_author('Tolkien'))