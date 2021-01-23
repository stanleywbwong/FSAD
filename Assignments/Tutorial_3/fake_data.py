from datetime import datetime, timedelta

dogs = [
    {
        "name" : "Melba",
        "handle" : "melba",
        "bio" : "Hi, I'm Melba! I'm a mini-goldendoodle and I love to play.",
        "age" : 3
    },
    {
        "name" : "Charlie",
        "handle" : "chucky",
        "bio" : "Hi I'm Charlie! I'm a big white standard poodle.",
        "age" : 7
    },
    {
        "name" : "Rosie",
        "handle" : "rose",
        "bio" : "Hi I'm Rosie! I'm from the hard streets of LA, don't mess with me.",
        "age" : 9
    }
]

def get_dog_by_handle(handle):
    for dog in dogs:
        if dog['handle'] == handle:
            return dog

posts = [
    {
        "handle": "melba", 
        "text": "I'm so excited to move to California!", 
        "liked": ["chucky", "rose"],
        "time": "01/22/2021, 20:47:05"
    },
    {
        "handle": "melba", 
        "text": "Great game of fetch today with my Dad, Paul", 
        "liked": ["chucky"],
        "time": "01/22/2021, 05:04:31"
    },
    {
        "handle": "chucky", 
        "text": "Took a great 8 hour nap today, then guarded the household", 
        "liked": ["rose", "melba"],
        "time": "01/20/2021, 00:00:00"
    },
    {
        "handle": "melba", 
        "text": "Peanut butter is my favorite snack!", 
        "liked": ["rose", "chucky", "melba"],
        "time": "01/13/2021, 12:54:33"
    },
    {
        "handle": "rose", 
        "text": "Today I stole food from a blind dog.", 
        "liked": [],
        "time": "12/12/2018, 04:42:20"
    }
]

def get_posts_by_handle(handle):
    return [post for post in posts if post['handle'] == handle]

def format_likes(post):
    likes = post["liked"]
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

def format_time(post):
    time_posted = datetime.strptime(post["time"], '%m/%d/%Y, %H:%M:%S')
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