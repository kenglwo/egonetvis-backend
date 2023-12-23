
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
import MySQLdb

app = Flask(__name__)

DB_HOST = "egonetvis.mysql.pythonanywhere-services.com"
DB_USER = "egonetvis"
DB_PASSWD = "raing9Ej"
DB_NAME = "egonetvis$data"

def get_db_cursor(host, user, passwd, db): 
    db = MySQLdb.connect(host, user, passwd, db)
    cursor = db.cursor()
    return cursor


@app.route('/')
def hello_world():
    cursor = get_db_cursor(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
    cursor.execute("select name from test limit 1")
    output = ""
    for res in cursor:
        print(res)
        output += res[0]
    cursor.close()

    return output

@app.route('/test', methods=["GET", "POST"])
def test():
    if (request.method == 'POST'):
        name = request.form.get('name')
        age = int(request.form.get('age'))

        cursor = get_db_cursor(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
        # insert the values
        sql = "insert into test values('{}', {})".format(name, age)
        cursor.execute(sql)

        # fetch all data
        cursor.execute("select name, age from test")
        output = '''
            <table>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                </tr>
                tablerow
            </table>
        '''

        data = ""
        for res in cursor:
            name = res[0]
            age = res[1]
            data += "<tr><td>{}</td><td>{}</td></tr>".format(name, age)

        output = output.replace("tablerow", data)
        cursor.close()

        return output

    return render_template('test.html')

