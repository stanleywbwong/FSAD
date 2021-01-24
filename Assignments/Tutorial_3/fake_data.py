from datetime import datetime, timedelta
import re

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

# def format_post(post):
#     text = post["text"]
#     handles = [f"@{dog["handle"]}" for dog in dogs]
#     # use regex to replace text with appropriate html

def get_dog_by_handle(handle):
    for dog in dogs:
        if dog['handle'] == handle:
            return dog

def get_posts_by_handle(handle):
    return [post for post in posts if post['handle'] == handle]
