from flask import Flask, request, jsonify, render_template, session, g
import mysql.connector

app = Flask(__name__, static_url_path='/static')
app.config.update(SECRET_KEY='senhadoapp')

def create_connection():
    # Database information

    database_config = {
        'host': '162.241.155.7',
        'port': 3306,
        'user': 'ramaischiaperini_sisteminha',
        'password': 'h_Xjfm9R6#&a',
        'database': 'ramaischiaperini_sisteminha'
    }

    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**database_config)

        if connection.is_connected():
            print("Connected to the database!")
            return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

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

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('home.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/api/clientes', methods=['GET'])
def clientes_get():
    if 'logado' in session and session['logado']:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes')
        clientes = cur.fetchall()
        conn.close()
        return jsonify(clientes)
    else:
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
    cur.execute('INSERT INTO clientes(nome, perfil, telefone, whatsapp, periodo) VALUES (%s, %s, %s, %s, %s)', dados)
    conn.commit()
    conn.close()
    return jsonify({"status": 200, "message": "Client added successfully"}), 200

@app.route('/api/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        # Handle GET request (e.g., fetch users from the database)
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios')
        usuarios = cur.fetchall()
        conn.close()
        return jsonify(usuarios)
    elif request.method == 'POST':
        # Handle POST request (e.g., add a new user to the database)
        formulario = request.form
        dados = (
            formulario['usuario'],
            formulario['senha']
        )
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO usuarios(login, senha) VALUES (%s, %s)', dados)
        conn.commit()
        conn.close()
        return jsonify({"status": 200, "message": "User added successfully"}), 200


@app.route('/api/login', methods=['POST'])
def login():
    # Get the login and senha from the form data
    login = request.form.get('usuario')
    senha = request.form.get('senha')

    # Check the credentials against the database
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM membros WHERE login=%s AND senha=%s', (login, senha))
    user = cur.fetchone()
    conn.close()

    if user:
        # If the user is found, set session variables and return success
        session['logado'] = True
        session['usuario'] = login
        return jsonify({"status": 200, "message": "Login successful"}), 200
    else:
        # If the user is not found, return unauthorized
        return jsonify({"status": 401, "message": "Unauthorized"}), 401

@app.route('/api/clientes', methods=['DELETE'])
def clientes_delete():
    if 'logado' in session and session['logado']:
        formulario = request.form
        dados = (formulario['id'],)
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM clientes WHERE id=%s', dados)
        conn.commit()
        cur.execute('SELECT * FROM clientes')
        clientes = cur.fetchall()
        conn.close()
        return jsonify(clientes)
    else:
        return jsonify({"status": 400, "message": "Not logged in"}), 400

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    if 'logado' in session and session['logado']:
        conn = get_db()
        cur = conn.cursor()

        # Example query to fetch statistics (adjust as needed)
        cur.execute('SELECT COUNT(*) FROM usuarios')
        total_usuarios = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM clientes')
        total_clientes = cur.fetchone()[0]

        conn.close()

        return jsonify([total_usuarios, total_clientes])
    else:
        return jsonify({"status": 400, "message": "Not logged in"}), 400

    @app.route('/api/usuarios', methods=['DELETE'])
    def clientes_delete():
        if 'logado' in session and session['logado']:
            formulario = request.form
            dados = (formulario['usuarioId'],)
            conn = get_db()
            cur = conn.cursor()
            cur.execute('DELETE FROM usuarios WHERE id=%s', dados)
            conn.commit()
            cur.execute('SELECT * FROM usuarios')
            clientes = cur.fetchall()
            conn.close()
            return jsonify(usuarios)
        else:
            return jsonify({"status": 400, "message": "Not logged in"}), 400


if __name__ == "__main__":
    app.run(debug=True)
