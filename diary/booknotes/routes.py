from flask import render_template, current_app, url_for, jsonify, request, flash, redirect

from diary.booknotes import bp
from diary.diarydatabase import BookNotesDatabase


def get_db():
    return BookNotesDatabase(current_app.config['DBFILENAME'])


@bp.route('/booknotes_index')
def booknotes_index():
    books = get_db().book_get_all()
    return render_template('booknotes/index.html', books=books) 


@bp.route('/forms/add_book')
def form_add_book():
    if request.args:
        title = request.args.get('title')
        isbn = request.args.get('isbn')
        db = get_db()
        db.insert_book(title, isbn)
        flash(f"Added book {title}")
        return redirect(url_for('booknotes.booknotes_index'))
    return render_template('booknotes/form_add_book.html')


@bp.route('/booknotes/<id>')
def booknotes_page(id):
    db = get_db()
    if request.args:
        try:
            chapter = int(request.args.get('chapter'))
        except ValueError:
            flash('Error invalid id format')
            return redirect(url_for('booknotes.booknotes_page', id=id))
        title = request.args.get('title')
        db.insert_chapternotes(id, chapter, title, notes='')
        flash(f"Added blank note for {title}")
        return redirect(url_for('booknotes.booknotes_page', id=id))
    book = db.get_book(id)
    chapters = db.book_get_chapternotes(id)
    return render_template('booknotes/booknotes.html', book=book, chapters=chapters)


@bp.route('/chapter/<id>')
def chapter_page(id):
    db = get_db()
    chapter = db.get_chapter(id)
    book_id = chapter['book_id']
    book = db.get_book(book_id)
    if request.args:
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash('Error invalid id format')
            return redirect(url_for('booknotes.chapter_page', id=id))
        notes = request.args.get('notes')
        # TODO calling this too many times
        chapter = db.get_chapter(id)
        chapter['notes'] = notes
        db.update_chapternotes(**chapter)
        flash(f"Updated notes for {book['title']}: {chapter['chapter_title']}")
        return redirect(url_for('booknotes.booknotes_page', id=book_id))
    
    return render_template('booknotes/chapter.html', chapter=chapter, book=book)
