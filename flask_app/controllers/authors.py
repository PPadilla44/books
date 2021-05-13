from flask_app.models.book import Book
from flask_app import app
from flask import render_template,redirect,request

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.author import Author

@app.route('/')
def index_redirect():
    return redirect('/authors')

@app.route('/authors')
def show_authors():
    return render_template("author_list.html", all_authors = Author.get_all())

@app.route('/authors/create', methods=['POST'])
def create_author():
    Author.save(request.form)
    return redirect('/authors')

@app.route('/authors/<author_id>')
def author_fave(author_id):
    data = {
        'id': author_id
    }
    return render_template("author_fave.html", author=Author.get_author_by_id_with_books(data), all_books=Book.get_all())

@app.route('/authors/<authorid>/addfave',methods=['POST'])
def add_fave(authorid):
    data = {
        'authorid': authorid,
        'bookid': request.form['bookfave']
    }
    Author.add_fave(data)
    return redirect(f'/authors/{authorid}')