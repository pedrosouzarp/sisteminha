import sqlite3
from flask import Flask, request, json, jsonify, render_template, session, g

DATABASE = './database/banco.sqlite'
app = Flask(__name__)
app.config.update(SECRET_KEY='senhadoapp')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/api/clientes', methods=['GET'])
def clientes_get():
    if (session['logado'] == True):
        conn = get_db()
        cur = conn.cursor()
        clientes = cur.execute('select * from clientes').fetchall()
        conn.close()
        return jsonify(clientes)
    else:
        return app.response_class(
            status=400
        )


@app.route('/api/clientes', methods=['POST'])
def clientes_post():
    formulario = request.form
    dados = (
        formulario['nome'],
        formulario['perfil'],
        formulario['telefone'].replace(
            '(', '').replace(')', '').replace(' ', '').replace('-', ''),
        formulario['whatsapp'].replace(
            '(', '').replace(')', '').replace(' ', '').replace('-', ''),
        formulario['periodo']
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'insert into clientes(nome,perfil,telefone,whatsapp,periodo) values (?,?,?,?,?)', dados)
    conn.commit()
    conn.close()
    return app.response_class(
        status=200
    )

@app.route('/api/clientes', methods=['DELETE'])
def clientes_delete():
    if (session['logado'] == True):
        formulario = request.form
        dados = (
            formulario['id'],
        )
        conn = get_db()
        cur = conn.cursor()
        deleta = cur.execute('delete from clientes where id=?', dados)
        conn.commit()
        clientes = cur.execute('select * from clientes').fetchall()
        conn.close()
        return jsonify(clientes)
    else:
        return app.response_class(
            status=400
        )


@app.route('/api/usuarios', methods=['GET'])
def usuarios_get():
    if (session['logado'] == True):
        conn = get_db()
        cur = conn.cursor()
        usuarios = cur.execute('select * from usuarios where id != 1').fetchall()
        conn.close()
        return jsonify(usuarios)
    else:
        return app.response_class(
            status=400
        )


@app.route('/api/usuarios', methods=['POST'])
def usuarios_post():
    if (session['logado'] == True):
        formulario = request.form
        dados = (
            formulario['usuario'],
            formulario['senha'],
        )
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'insert into usuarios(login,senha) values (?,?)', dados)
        conn.commit()
        usuarios = cur.execute('select * from usuarios where id != 1').fetchall()
        conn.close()
        return jsonify(usuarios)
    else:
        return app.response_class(
            status=400
        )

@app.route('/api/usuarios', methods=['DELETE'])
def usuarios_delete():
    if (session['logado'] == True):
        formulario = request.form
        if (formulario['id'] == 1):
            return app.response_class(
                status=400
            )
        dados = (
            formulario['id'],
        )
        conn = get_db()
        cur = conn.cursor()
        deleta = cur.execute('delete from usuarios where id=?', dados)
        conn.commit()
        usuarios = cur.execute('select * from usuarios').fetchall()
        conn.close()
        return jsonify(usuarios)
    else:
        return app.response_class(
            status=400
        )


@app.route('/api/login', methods=['POST'])
def login():
    formulario = request.form
    dados = (
        formulario['usuario'],
        formulario['senha'],
    )
    conn = get_db()
    cur = conn.cursor()
    usuarios = cur.execute(
        'select * from usuarios where login=? and senha=?', (dados)).fetchall()
    conn.close()
    if (usuarios):
        session['logado'] = True
        session['usuario'] = usuarios[0][1]
        return app.response_class(
            status=200
        )
    else:
        return app.response_class(
            status=400
        )


@app.route('/api/logout', methods=['POST'])
def logout():
    if (session['logado'] == True):
        session['logado'] = False
        return app.response_class(
            status=200
        )
    else:
        return app.response_class(
            status=400
        )

@app.route('/api/estatisticas', methods=['GET'])
def total():
    if (session['logado'] == True):
        conn = get_db()
        cur = conn.cursor()
        usuarios = cur.execute('select * from usuarios').fetchall()
        clientes = cur.execute('select * from clientes').fetchall()
        conn.close()
        total = [
            len(usuarios),
            len(clientes)
        ]
        return jsonify(total)

    else:
        return app.response_class(
            status=400
        )
