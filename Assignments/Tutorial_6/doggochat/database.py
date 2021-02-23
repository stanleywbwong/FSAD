import pyodbc
from config import server, database, username, password

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                        ';DATABASE='+database+
                        ';UID='+username+
                        ';PWD='+password)

cursor = conn.cursor()

def get_all_posts():
    cursor.execute("""
    SELECT
        Posts.Id,
        Posts.Handle,
        Posts.Text,
        Posts.Time,
        Dogs.Name,
        LikeCountQueryResult.LikeCount

    FROM Posts

    INNER JOIN Dogs ON Posts.Handle = Dogs.Handle

    INNER JOIN (
        SELECT
            Posts.Id, 
            COUNT(Likes.Handle) AS LikeCount
        FROM Posts
        LEFT JOIN Likes
            ON Posts.Id = Likes.PostId
        GROUP BY Id) LikeCountQueryResult 
    ON LikeCountQueryResult.Id = Posts.Id
    
    ORDER BY Posts.Time DESC""")

    columns = [column[0] for column in cursor.description]
    posts = [dict(zip(columns, row)) for row in cursor]
    return posts

def get_posts_by_handle(handle):
    all_posts = get_all_posts()
    posts = [post for post in all_posts if post['Handle'] == handle]
    return posts

def get_dog_by_handle(handle):
    cursor.execute("SELECT * from Dogs WHERE Handle = ?", handle)
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None

def get_password(username):
    cursor.execute("SELECT Dogs.Password FROM Dogs WHERE Handle = ?", username)
    row = cursor.fetchone()
    return row[0] if row else None

def insert_post(handle, post_content, time):
    cursor.execute("""INSERT INTO Posts ([Handle], [Text], [Time])
                        VALUES (?, ?, ?)""", handle, post_content, time)
    conn.commit()
    return True

def delete_post(post_id, handle):
    cursor.execute("DELETE FROM Posts WHERE ID = ? AND Handle = ?", post_id, handle)
    conn.commit()
    return True

def like_unlike(post_id, handle):
    cursor.execute("SELECT * FROM Likes WHERE PostId = ? AND Handle = ?", post_id, handle)
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM Likes WHERE PostId = ? AND Handle = ?", post_id, handle)
    else:
        cursor.execute("INSERT INTO Likes ([Handle], [PostId]) VALUES (?, ?)", handle, post_id)
    conn.commit()
    return True