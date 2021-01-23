from flask import Flask, render_template
from fake_data import *

app = Flask(__name__, template_folder="templates", static_url_path='/static')

@app.route('/')
def feed():
    return render_template('feed.html', 
                            posts=posts, 
                            get_dog_by_handle=get_dog_by_handle, 
                            format_likes=format_likes,
                            format_time=format_time)
    
@app.route('/dog/<string:handle>')
def dog(handle):
    dog = get_dog_by_handle(handle)
    return render_template('dog.html', 
                            dog=dog, 
                            posts=get_posts_by_handle(handle),
                            format_likes=format_likes,
                            format_time=format_time)

if __name__ == "__main__":
    app.run(debug=True)