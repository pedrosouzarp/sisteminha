from flask import Flask, request, json, jsonify, render_template, session, g
from conexao_bd import create_connection

app = Flask(__name__, static_url_path='/static')
app.config.update(SECRET_KEY='senhadoapp')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = create_connection()
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
    if 'logado' in session.keys():
        if session['logado'] == True:
            conn = get_db()
            cur = conn.cursor()
            clientes = cur.execute('select * from clientes').fetchall()
            conn.close()
            return jsonify(clientes)
        else:
            return jsonify({"status": 400, "message": "Not logged in"}), 400
    else:
        session['logado'] = False
        return jsonify({"status": 400, "message": "Not logged in"}), 400

@app.route('/api/clientes', methods=['POST'])
def clientes_post():
    formulario = request.form
    dados = (
        formulario['nome'],
        formulario['perfil'],
        formulario['telefone'].replace('(', '').replace(')', '').replace(' ', '').replace('-', ''),
        formulario['whatsapp'].replace('(', '').replace(')', '').replace(' ', '').replace('-', ''),
        formulario['periodo']
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute('insert into clientes(nome,perfil,telefone,whatsapp,periodo) values (?,?,?,?,?)', dados)
    conn.commit()
    conn.close()
    return jsonify({"status": 200, "message": "Client added successfully"}), 200

@app.route('/api/clientes', methods=['DELETE'])
def clientes_delete():
    if 'logado' in session.keys():
        if session['logado'] == True:
            formulario = request.form
            dados = (formulario['id'],)
            conn = get_db()
            cur = conn.cursor()
            cur.execute('delete from clientes where id=?', dados)
            conn.commit()
            clientes = cur.execute('select * from clientes').fetchall()
            conn.close()
            return jsonify(clientes)
        else:
            return jsonify({"status": 400, "message": "Not logged in"}), 400
    else:
        session['logado'] = False
        return jsonify({"status": 400, "message": "Not logged in"}), 400

# Your other routes go here

if __name__ == "__main__":
    app.run(debug=True)
