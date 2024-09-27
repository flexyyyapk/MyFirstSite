from flask import Flask, render_template, request, jsonify
from db import DataBase
import json

app = Flask(__name__)
db = DataBase()

@app.route('/')
def main_menu():
    return render_template('index.html')

@app.route('/add_comments')
def add_comments():
    comments = db.c.execute('SELECT * FROM forum').fetchall()
    print(comments)

    jsons = {}
    for comment in comments:
        jsons.update({str(comment[0]): {"heading": comment[1], "subtitle": comment[2], "comments": comment[3]}})

    print(json.dumps(jsons))
    return json.dumps(jsons)

@app.route('/forum_id=<int:id>')
def forum(id):
    return render_template('forum.html', id=id)

@app.route('/forum_id=<int:id>/add_comment', methods=['POST'])
def add_comment(id):
    data = request.json
    comments = eval(db.c.execute('SELECT comments FROM forum WHERE id = ?', (id,)).fetchone()[0])
    comments.append({"id": str(int(comments[-1]['id'])+1 if comments else 0), "name": data['name'], "comment": data['comment']})

    db.c.execute('UPDATE forum SET comments = ? WHERE id = ?', (str(comments), id))
    db.conn.commit()
    return render_template('forum.html', id=id)

@app.route('/create_post')
def create_post():
    return render_template('create_post.html')

@app.route('/public_post', methods=['POST'])
def public_post():
    data = request.json

    posts = db.c.execute('SELECT id FROM forum').fetchall()

    last_id = 0 if posts is None else posts[-1][0]+1
    print(last_id)

    db.c.execute('INSERT INTO forum(id, heading, subtitle, comments) VALUES(?, ?, ?, ?)', (last_id, data['heading'], data['subtitle'], '[]'))
    db.conn.commit()

    return json.dumps({"id": last_id})

app.run(debug=True, host='0.0.0.0', port=5000)