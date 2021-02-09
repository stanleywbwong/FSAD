from flask import Flask, render_template
from datetime import datetime, timedelta
from database import *

import re

app = Flask(__name__, template_folder="templates", static_url_path='/static')

@app.route('/')
def feed():
    posts = get_all_posts()
    handles = set([post["Handle"] for post in posts])
    return render_template('feed.html', 
                            posts=posts,
                            handles=handles)
    
@app.route('/dog/<string:handle>')
def dog(handle):
    dog = get_dog_by_handle(handle)
    posts = get_posts_by_handle(handle)
    handles = set([post["Handle"] for post in posts])
    return render_template('dog.html',
                            dog=dog,
                            posts=posts,
                            handles=handles)

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