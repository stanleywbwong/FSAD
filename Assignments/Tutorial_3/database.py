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
    cursor.execute('SELECT [Handle],[Text],[Time] from Posts')

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
    cursor.execute(f"SELECT * from Posts WHERE Handle = '{handle}'")

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
    cursor.execute(f"SELECT * from Dogs WHERE Handle = '{handle}'")

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns, row))
        results.append(d)

    if len(results):
        return results[0]

    return None