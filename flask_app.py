
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)

PROD = False

DB_HOST_PROD = "egonetvis.mysql.pythonanywhere-services.com"
DB_USER_PROD = "egonetvis"
DB_PASSWD_PROD = "raing9Ej"
DB_NAME_PROD = "egonetvis$data"

DB_HOST_LOCAL = "localhost"
DB_USER_LOCAL = "root"
DB_PASSWD_LOCAL = ""
DB_NAME_LOCAL = "SampleDB"

if PROD:
    DB_HOST = DB_HOST_PROD
    DB_USER = DB_USER_PROD
    DB_PASSWD = DB_PASSWD_PROD
    DB_NAME = DB_NAME_PROD
else:
    DB_HOST = DB_HOST_LOCAL
    DB_USER = DB_USER_LOCAL
    DB_PASSWD = DB_PASSWD_LOCAL
    DB_NAME = DB_NAME_LOCAL

def get_db_cursor(host, user, passwd, db):
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = db.cursor()
    return [db, cursor]

@app.route('/')
def hello_world():
    db, cursor = get_db_cursor(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)

    output = ""
    try:
        cursor.execute("select name from test limit 1")
        for res in cursor:
            print(res)
            output += res[0]
    except Exception:
        output = "DB Error: unable to fetch items"

    finally:
        cursor.close()
        db.close()
        return output
    

@app.route('/test', methods=["GET", "POST"])
def test():
    if (request.method == 'POST'):
        name = request.form.get('name')
        age = int(request.form.get('age'))

        output = ""
        db, cursor = get_db_cursor(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)

        try:
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
            cursor.execute(sql)
        except Exception:
            output = "DB Error: unable to fetch items"

        finally:
            cursor.close()
            db.close()
            return output

    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
