from flask_app.models.author import Author
from flask_app.config.mysqlconnection import connectToMySQL

class Book:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO books(title,num_of_pages,created_at,updated_at) \
        VALUES (%(title)s,%(pages)s, NOW(), NOW());"
        return connectToMySQL('books_schema').query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM books WHERE books.id = %(id)s"
        results = connectToMySQL('books_schema').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_book_by_id_with_authors(cls,data):
        from flask_app.models.author import Author
        query = "SELECT * FROM books JOIN favorites on books.id = favorites.books_id \
        JOIN authors on authors.id = favorites.author_id WHERE books.id = %(id)s  GROUP BY authors.id ;"
        results = connectToMySQL('books_schema').query_db(query,data)
        if results:
            book = cls(results[0])
            for row in results:
                data = {
                    'id': row['authors.id'],
                    'name': row['name'],
                    "created_at": row['authors.created_at'],
                    "updated_at": row['authors.updated_at'],
                }
                book.authors.append(Author(data))
        else:
            book = Book.get_by_id(data)
        return book

    @classmethod
    def add_fave(clas,data):
        query = "INSERT INTO favorites(author_id,books_id) \
        VALUES (%(authorid)s,%(bookid)s);"
        return connectToMySQL('books_schema').query_db(query,data)