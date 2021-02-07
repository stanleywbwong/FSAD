import pyodbc

server = "tcp:dogchat-stan.database.windows.net"
database = "dogchat"
username = "stanwong"
password = "Swong394!"

def get_all_posts():
    
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                          ';DATABASE='+database+
                          ';UID='+username+
                          ';PWD='+password)

    cursor = conn.cursor()
    cursor.execute("""
    SELECT
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
    ON LikeCountQueryResult.Id = Posts.Id""")

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns, row))
        results.append(d)

    return results

def get_posts_by_handle(handle):
    
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                          ';DATABASE='+database+
                          ';UID='+username+
                          ';PWD='+password)

    cursor = conn.cursor()
    cursor.execute("SELECT * from Posts WHERE Handle = ?", handle)

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns, row))
        results.append(d)

    return results

def get_dog_by_handle(handle):

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                          ';DATABASE='+database+
                          ';UID='+username+
                          ';PWD='+password)

    cursor = conn.cursor()
    cursor.execute("SELECT * from Dogs WHERE Handle = ?", handle)

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns, row))
        results.append(d)

    if len(results):
        return results[0]

    return None