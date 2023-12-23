
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)

# db = MySQLdb.connect(
#     # host = "egonetvis.mysql.pythonanywhere-services.com",
#     host = "localhost",
#     user = "egonetvis",
#     passwd = "raing9Ej",
#     db = "egonetvis$data"
# )
db = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='',
                           db='SampleDB')
cursor = db.cursor()

@app.route('/')
def index():
    # cursor.execute("select name from test limit 1")
    # output = ""
    # for res in cursor:
    #     print(res)
    #     output += res[0]
    # return output
    return "Hello World!"

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
