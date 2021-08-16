import os
import json

from flask import render_template, url_for, request, flash, redirect
import requests
from requests.exceptions import ConnectionError

from diary.articles import bp


@bp.route('/articles_index')
def articles_index():
    api_url = os.environ["ARTICLES_API_URL"]
    # Obtain from API
    try:
        response = requests.get(api_url + "/articles")
    except ConnectionError:
        articles = []
        flash("articles cannot be displayed as articles service is not available at the moment")
    else:
        articles = json.loads(response.content).values()

    # Adding an article
    if request.args:
        url = request.args.get('url')
        if not url:
            flash('url must not be blank')
            return render_template('articles/index.html', articles=articles)

        # Add through API
        try:
            post_response = requests.post(api_url + "/articles",
                                        data={"url": url})
        except ConnectionError:
            flash("article could not be added as articles service is not available at the moment")
        else:
            flash(f'Added article: {url}')
        return redirect(url_for('articles.articles_index'))
    return render_template('articles/index.html', articles=articles)
