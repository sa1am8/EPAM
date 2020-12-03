import sqlite3
import pdb
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()


'''@app.before_request
def init_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/db.qslite3'
    db = SQLAlchemy(app)
    g.db = SQLAlchemy(app)
    migrate = Migrate(app, g.db)


@app.after_request
def close_db(r):
    g.db.close()
    return r
'''

@app.route('/posts', methods=['GET'])
def get_all():
    cursor = db.execute('select id, name, body from blog')
    posts = cursor.fetchall()
    posts = [{'id': id_, 'name': name, 'body': body} for id_, name, body in posts]
    return jsonify(posts)


@app.route('/posts/<int:id_>', methods=['GET'])
def get(id_):
    cursor = g.db.execute('select id, name, body from blog where id=?', (id_,))
    post = cursor.fetchone()
    if post is None:
        return jsonify({'message': 'Not found'}), 404
    post = [{'id': post[0], 'name': post[1], 'body': post[2]}]
    return jsonify(post)


@app.route('/posts', methods=['POST'])
def post_():
    name = request.json['name']
    body = request.json['body']
    cursor = db.execute('insert into blog (name, body) values (?, ?)', (name, body))
    db.commit()
    return jsonify({'id_': cursor.lastrowid, 'name': name, 'body': body}), 201


@app.route('/posts/<int:id_>', methods=['PUT'])
def put(id_):
    cursor = db.execute('select name, body from blog where id=?', (id_,))
    post = cursor.fetchone()
    if post is None:
        return jsonify({'message': 'Not found'}), 404
    name = request.json.get('name', post[0])
    body = request.json.get('body', post[1])
    db.execute('update blog set name=?, body=? where id=?', (name, body, id_))
    db.commit()
    return jsonify(''), 204


@app.route('/posts/<int:id_>', methods=['DELETE'])
def delete(id_):
    cursor = db.execute('delete from blog where id=?', (id_,))
    if not cursor.rowcount:
        return jsonify({'message': 'Not found'}), 404
    db.commit()
    return jsonify(''), 204


@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = db.execute(
        "select name, body from blog order by id desc"
    )
    posts = cursor.fetchall()
    if request.method == 'POST':
        name = request.form.get('name', '')
        body = request.form.get('body', '')
        if name and body:
            cursor = db.cursor()
            cursor.execute(
                "insert into blog (name, body) values (?, ?)",
                (name, body)
            )
            cursor.close()
            db.commit()
            return redirect('/')

    db.close()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
