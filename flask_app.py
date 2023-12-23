
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
import MySQLdb

app = Flask(__name__)

db = MySQLdb.connect(
    host = "egonetvis.mysql.pythonanywhere-services.com",
    user = "egonetvis",
    passwd = "raing9Ej",
    db = "egonetvis$data"
)

cursor = db.cursor()

@app.route('/')
def hello_world():
    cursor.execute("select name from test limit 1")
    output = ""
    for res in cursor:
        print(res)
        output += res[0]

    return output

@app.route('/test', methods=["GET", "POST"])
def test():
    if (request.method == 'POST'):
        name = request.form.get('name')
        age = int(request.form.get('age'))

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

        return output

    return render_template('test.html')
