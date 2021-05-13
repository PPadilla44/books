from flask_app.models.author import Author
from flask_app import app
from flask import render_template,redirect,request

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book

@app.route('/books')
def show_books():
    return render_template("book_list.html", all_books = Book.get_all())

@app.route('/books/create', methods=['POST'])
def create_book():
    Book.save(request.form)
    return redirect('/books')

@app.route('/books/<bookid>')
def book_fave(bookid):
    data = {
        'id': bookid
    }
    return render_template("book_fave.html", book=Book.get_book_by_id_with_authors(data), all_authors=Author.get_all())

@app.route('/books/<bookid>/addfave', methods=['POST'])
def add_fave_book(bookid):
    data = {
        'authorid': request.form['authorfave'],
        'bookid': bookid
    }
    Book.add_fave(data)
    return redirect(f'/books/{bookid}')