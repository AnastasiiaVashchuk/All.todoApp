import os
import hashlib


def get_database_connection():
    '''
        Creates a connection between selected database
    '''
    import sqlite3
    sqlite_file = "todo.db"
    file_exists = os.path.isfile(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    if not file_exists:
        create_sqlite_tables(conn)
    return conn


def create_sqlite_tables(conn):
    '''
        Creates a sqlite table as specified in schema_sqlite.sql file
    '''
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
        print(1111)
    conn.commit()


def get_user_count():
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def check_user_exists(username, password):
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def store_last_login(user_id):
    '''
        Checks whether a user exists with the specified username and password
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login=(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id=?",
                       (user_id,))
        conn.commit()
        cursor.close()
    except:
        cursor.close()


def check_username(username):
    '''
        Checks whether a username is already taken or not
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            return True
    except:
        return False


def signup_user(username, password, email):
    '''
        Function for storing the details of a user into the database
        while registering
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_user_data(user_id):
    '''
        Function for getting the data of a specific user using his user_id
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (str(user_id),))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()


def get_data_using_user_id(id):
    '''
        Function for getting the data of all tasks using user_id
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE user_id=' + str(id,))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()


def get_data_using_id(id):
    '''
        Function for retrieving data of a specific task using its id
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        return results[0]
    except:
        cursor.close()


def get_number_of_tasks(id):
    '''
         Function for retrieving number of tasks stored by a specific user
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(task) FROM tasks WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()


def get_data():
    '''
        Function for getting data of all tasks
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def add_task(task, project_id, status, deadline,priority,user_id):
    '''
        Function for adding task into the database
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks( task, project_id, done, deadline, priority, user_id) VALUES (?, ?, ?, ?, ?,?)",
                       (task, project_id, status, deadline,priority, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def edit_task( name,project,status,deadline, priority, id):
    '''
        Function for updating task data in the database
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET task=?, project_id=?, done=coalesce(?,done), deadline=?,  priority=?  WHERE id=?", (name,project,status,deadline, priority, id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def delete_task_using_id(id):
    '''
        Function for deleting a specific task using its id
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def generate_password_hash(password):
    '''
        Function for generating a password hash
    '''
    hashed_value = hashlib.md5(password.encode())
    return hashed_value.hexdigest()


def add_project(name, user_id):
    '''
        Function for adding a projecy into the database
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects(project, user_id) VALUES (?, ?)", (name, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def edit_project( name, id):
    '''
        Function for updating project data in the database
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE projects SET project=?  WHERE id=?", (name,id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_all_projects(user_id):
    '''
        Function for getting all projects for a specific user
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, project FROM projects WHERE user_id=?', (str(user_id),))
        results = cursor.fetchall()
        if len(results) > 0:
            results = [(str(results[i][0]), results[i][1]) for i in range(len(results))]
        else:
            results = None
        cursor.close()
        return results
    except:
        cursor.close()



def get_data_using_project_id(id):
    '''
       Function for retrieving data of a specific project using its id
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT project FROM projects WHERE id=?', (str(id),))
        results = cursor.fetchone()
        cursor.close()
        return results
    except:
        cursor.close()


def delete_project_using_id(id):
    '''
        Function for deleting a specific project using its id
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_number_of_projects(id):
    '''
        Function for retrieving number of projects stored by a specific user
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(project) FROM projects WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()


def edit_email(email, user_id):
    '''
        Function for updating email in the database
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE id=?", (email, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def edit_password(password, user_id):
    '''
         Function for updating password in the database
    '''
    global cursor
    conn = get_database_connection()
    password = generate_password_hash(password)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE id=?", (password, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_search_data(pattern, user_id):
    '''
        Function for searching task based on specified pattern
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id=? AND note_title LIKE ? LIMIT 3",
                       (user_id, '%' + pattern + '%'))
        results = cursor.fetchall()
        results = [(results[i][0], results[i][3]) for i in range(len(results))]
        cursor.close()
        return results
    except:
        cursor.close()


def get_rest_data_using_user_id(id):
    '''
        Function for getting the data of all notes using user_id using REST
    '''
    global cursor
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE user_id=' + str(id))
        results = cursor.fetchall()
        fieldnames = [f[0] for f in cursor.description]
        cursor.close()
        if len(results) == 0:
            return None
        else:
            outer = {}
            for i in range(len(results)):
                data = {}
                for j in range(len(results[0])):
                    data[fieldnames[j]] = results[i][j]
                outer[int(i)] = data

            return outer
    except:
        cursor.close()
