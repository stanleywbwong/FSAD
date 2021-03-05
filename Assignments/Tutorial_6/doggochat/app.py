import flask
from flask import Flask, render_template, abort, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, FileField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from database import *
from urllib.parse import urlparse, urljoin
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

import re, os, uuid
import dog_email, config

app = Flask(__name__, template_folder="templates", static_url_path='/static')
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User():
    def __init__(self, username):
        dog = get_dog_by_handle(username)
        self.username = username
        self.avatar_image_name = dog['AvatarImageName']

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def get(cls, username):
        return User(username)

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('Username')
    name = StringField('Name')
    bio = TextAreaField('Bio')
    age = IntegerField('Age')
    avatar = FileField('Avatar')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    reset_password_form = ResetPasswordForm()
    if form.validate_on_submit():

        db_password = get_password(form.username.data)
        if db_password and check_password_hash(db_password, form.password.data):   
            user = User(form.username.data) 
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)

        return flask.redirect(next or flask.url_for('feed'))
    return flask.render_template('login.html', form=form, reset_password_form=reset_password_form)


@app.route('/feed')
@login_required
def feed():
    user = get_dog_by_handle(current_user.username)
    if not user:
        print('invalid user in database, using rose')
        user = get_dog_by_handle('rose')
    posts = get_all_posts()
    handles = set([post["Handle"] for post in posts])
    avatar_image_name = current_user.avatar_image_name
    avatar_url = 'https://doggochatstorage.blob.core.windows.net/dogavatars/' + current_user.avatar_image_name
    return render_template('feed.html',
                            user=user,
                            posts=posts,
                            handles=handles,
                            avatar_url=avatar_url)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():

        create_user(form.username.data, 
                    form.name.data,
                    form.bio.data, 
                    form.age.data, 
                    generate_password_hash(form.password.data),
                    form.avatar.data.filename)

        blob_service_client = BlobServiceClient.from_connection_string(config.blob_cnxn)
        blob_client = blob_service_client.get_blob_client(container=config.blob_container, blob=form.avatar.data.filename)
        blob_client.upload_blob(form.avatar.data)

        user = User(form.username.data) 
        login_user(user)

        # TODO: validate
        # * not existing user
        # * username/password are valid (non-empty strings)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)
        
        return flask.redirect(next or flask.url_for('feed'))
    return render_template('signup.html', form=form)

@app.route("/reset_password", methods=['POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        dog_email.reset_password(username)
        return 'Password successfully reset, check your email'
    else:
        return 'Failed to reset password'

@app.route('/dog/<string:handle>')
@login_required
def dog(handle):
    dog = get_dog_by_handle(handle)
    user = get_dog_by_handle(current_user.username)
    posts = get_posts_by_handle(handle)
    handles = set([post["Handle"] for post in posts])
    return render_template('dog.html',
                            dog=dog,
                            user=user,
                            posts=posts,
                            handles=handles)

@app.route('/create', methods=['POST'])
@login_required
def create():
    post_content = request.form['post-content']
    page = request.form['page']
    insert_post(current_user.username, post_content, datetime.now())
    if page == 'feed':
        return redirect(url_for(page))
    elif page == 'dog':
        handle = request.form['handle']
        return redirect(url_for(page, handle=handle))

@app.route('/change_like', methods=['POST'])
@login_required
def change_like():
    post_id = request.form['post-id']
    page = request.form['page']
    like_unlike(post_id, current_user.username)
    if page == 'feed':
        return redirect(url_for(page))
    elif page == 'dog':
        handle = request.form['handle']
        return redirect(url_for(page, handle=handle))

@app.route('/delete')
@login_required
def delete():
    post_id = request.args.get('post_id')
    page = request.args.get('page')
    delete_post(post_id, current_user.username)
    if page == 'feed':
        return redirect(url_for(page))
    elif page == 'dog':
        handle = request.args.get('handle')
        return redirect(url_for(page, handle=handle))

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('splash'))


# Register filters to use rather than passing functions into render_template function

@app.template_filter('datetime_filter')
def format_time(post, format="%m/%d/%Y, %H:%M:%S"):
    """Converts a post's time to appropriate format"""
    time_posted = post["Time"]
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