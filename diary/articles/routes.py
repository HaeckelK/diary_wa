from flask import render_template, current_app, url_for, jsonify, request, flash, redirect

from diary.articles import bp
from diary.diarydatabase import ArticleDatabase
from diary.utils import datestamp


def get_db():
    return ArticleDatabase(current_app.config['DBFILENAME'])


@bp.route('/articles_index')
def articles_index():
    articles = get_db().get_all_article()
    if request.args:
        url = request.args.get('url')
        if not url:
            flash('url must not be blank')
            return render_template('articles/index.html', articles=articles)
        db = get_db()
        db.insert_article(url, datestamp())
        flash('Added article')
        return redirect(url_for('articles.articles_index'))
    return render_template('articles/index.html', articles=articles)
