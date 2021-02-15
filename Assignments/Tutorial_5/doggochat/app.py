from flask import Flask, render_template, abort, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from database import *

import re

app = Flask(__name__, template_folder="templates", static_url_path='/static')
auth = HTTPBasicAuth()

users = {
    "melba": generate_password_hash("melba"),
    "rose": generate_password_hash("rose"),
    "chucky": generate_password_hash("chucky") 
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/feed')
@auth.login_required
def feed():
    posts = get_all_posts()
    handles = set([post["Handle"] for post in posts])
    return render_template('feed.html', 
                            posts=posts,
                            handles=handles,
                            user=auth.current_user())

@app.route('/dog/<string:handle>')
@auth.login_required
def dog(handle):
    dog = get_dog_by_handle(handle)
    posts = get_posts_by_handle(handle)
    handles = set([post["Handle"] for post in posts])
    return render_template('dog.html',
                            dog=dog,
                            posts=posts,
                            handles=handles)

@app.route('/create', methods=['POST'])
@auth.login_required
def create():
    post_content = request.form['post-content']
    current_time = datetime.strftime(datetime.now(), '%m/%d/%Y, %H:%M:%S')
    insert_post(auth.current_user(), post_content, current_time)
    return redirect(url_for('feed'))

@app.route('/delete')
@auth.login_required
def delete():
    post_id = request.args.get('post_id')
    delete_post(post_id, auth.current_user())
    return redirect(url_for('feed'))

@app.route('/')
@auth.login_required(optional=True)
def splash():
    if auth.current_user():
        return redirect(url_for('feed'))
    else:
        return render_template('splash.html')

@app.route('/logout')
def logout():
    return render_template('splash.html'), 401

# Register filters to use rather than passing functions into render_template function

@app.template_filter('datetime_filter')
def format_time(post, format="%m/%d/%Y, %H:%M:%S"):
    """Converts a post's time to appropriate format"""
    time_posted = datetime.strptime(post["Time"], '%m/%d/%Y, %H:%M:%S')
    time_now = datetime.now()
    time_since = time_now - time_posted
    if time_since < timedelta(minutes=1):
        return f"{time_since.seconds}s"
    elif time_since < timedelta(hours=1):
        return f"{time_since.seconds%3600//60}m"
    elif time_since < timedelta(days=1):
        return f"{time_since.seconds//3600}h"
    elif time_since < timedelta(weeks=1):
        return f"{time_since.days}d"
    elif time_since < timedelta(days=365):
        return f"{time_since.days//7}w"
    else:
        return f"{time_since.days//365}y"

@app.template_filter('like_filter')
def format_likes(post):
    """Formats likers of a post to an appropriate string to display"""
    likes = post["Likes"]
    if not likes:
        return ""
    elif len(likes) == 1:
        return f"Liked by {likes[0]}"
    elif len(likes) == 2:
        return f"Liked by {likes[0]} and {likes[1]}"
    else:
        more_likes = len(likes)-2
        like_string = f"Liked by {likes[0]}, {likes[1]}, and {len(likes)-2} "
        if more_likes == 1:
            return like_string + "other"
        else:
            return like_string + "others"

if __name__ == "__main__":
    app.run(debug=True)