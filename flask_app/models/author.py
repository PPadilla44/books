from flask_app.config.mysqlconnection import connectToMySQL

class Author:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from authors;"
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO authors(name,created_at,updated_at) \
        VALUES (%(authorname)s, NOW(), NOW());"
        return connectToMySQL('books_schema').query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM authors WHERE authors.id = %(id)s"
        results = connectToMySQL('books_schema').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_author_by_id_with_books(cls,data):
        from flask_app.models.book import Book
        query = "SELECT * FROM authors JOIN favorites on \
        authors.id = favorites.author_id JOIN books on \
        books.id = favorites.books_id WHERE authors.id = %(id)s \
        GROUP BY books.id;"
        resutls = connectToMySQL('books_schema').query_db(query,data)
        if resutls: 
            author = cls(resutls[0])
            for row in resutls:
                data = {
                    'id': row['books.id'],
                    'title': row['title'],
                    'num_of_pages': row['num_of_pages'],
                    "created_at": row['books.created_at'],
                    "updated_at": row['books.updated_at'],
                }
                author.books.append(Book(data))
        else:
            author = Author.get_by_id(data)
        return author
    
    @classmethod
    def find_authors(cls,data):
        query = "SELECT * FROM authors WHERE id NOT IN \
        (SELECT author_id FROM favorites WHERE books_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query,data)
        return results

    @classmethod
    def add_fave(cls,data):
        query = "INSERT INTO favorites(author_id,books_id) \
        VALUES (%(authorid)s, %(bookid)s);"
        return connectToMySQL('books_schema').query_db(query,data)
