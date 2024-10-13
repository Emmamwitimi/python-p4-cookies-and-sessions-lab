#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Clear session data route
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Route to list all articles
@app.route('/articles')
def index_articles():
    articles = Article.query.all()  # Fetch all articles
    articles_data = [
        {
            'id': article.id,
            'title': article.title,
            'author': article.author,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'content': article.content,
            'date': article.date
        } for article in articles
    ]
    return jsonify(articles_data), 200

# Route to show an individual article by ID
@app.route('/articles/<int:id>')
def show_article(id):
    article = Article.query.get(id)  # Fetch the article by ID
    
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    # Initialize page views in session if not present
    session['page_views'] = session.get('page_views', 0)
    session['page_views'] += 1

    # If page view limit is reached, return an error
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Return the article's details, including all fields
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author': article.author,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date
    }), 200

if __name__ == '__main__':
    app.run(port=5555)
