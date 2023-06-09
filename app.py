import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Configurações do banco de dados
DATABASE = 'C:\Portaria\Portaria\Banco\portaria.db'

# Usuários e senhas
USUARIOS = {
    'erlopes': '1',
    'ncmedeiros': '123',
    'admin': 'admin',
    'usuario4': 'senha4'
}

app.secret_key = 'sua_chave_secreta'


def criar_tabela_registros():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data TEXT,
                            horario TEXT,
                            nome_motorista TEXT,
                            cpf TEXT,
                            placa TEXT,
                            nota_fiscal TEXT,
                            itens TEXT,
                            fornecedor TEXT,
                            destino TEXT,
                            horario_entrada TEXT,
                            horario_saida TEXT,
                            porteiro TEXT,
                            entrada_saida TEXT,
                            natureza_operacao TEXT
                        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela de registros: {str(e)}")


def obter_registros(data=None):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if data:
            cursor.execute("SELECT * FROM registros WHERE data = ?", (data,))
        else:
            cursor.execute("SELECT * FROM registros")

        registros = cursor.fetchall()
        conn.close()
        return registros
    except Exception as e:
        print(f"Ocorreu um erro ao obter os registros: {str(e)}")
        return None


def adicionar_registro(data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                       horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO registros (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino, horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                        horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o registro: {str(e)}")
        return False


def atualizar_registro(registro_id, data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                      horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''UPDATE registros SET data=?, horario=?, nome_motorista=?, cpf=?, placa=?, nota_fiscal=?, itens=?, fornecedor=?, destino=?, horario_entrada=?, horario_saida=?, porteiro=?, entrada_saida=?, natureza_operacao=?
                          WHERE id=?''',
                       (data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                        horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao, registro_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o registro: {str(e)}")
        return False


def excluir_registro(registro_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registros WHERE id=?", (registro_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ocorreu um erro ao excluir o registro: {str(e)}")
        return False
        





@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USUARIOS and password == USUARIOS[username]:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Usuário ou senha incorretos.'
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form['filtro_data']
        registros = obter_registros(data)
        return render_template('index.html', registros=registros)
    else:
        registros = obter_registros()
        return render_template('index.html', registros=registros)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    data = request.form['data']
    horario = request.form['horario']
    nome_motorista = request.form['nome_motorista']
    cpf = request.form['cpf']
    placa = request.form['placa']
    nota_fiscal = request.form['nota_fiscal']
    itens = request.form['itens']
    fornecedor = request.form['fornecedor']
    destino = request.form['destino']
    horario_entrada = request.form['horario_entrada']
    horario_saida = request.form['horario_saida']
    porteiro = request.form['porteiro']
    entrada_saida = request.form['entrada_saida']
    natureza_operacao = request.form['natureza_operacao']

    if adicionar_registro(data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor, destino,
                          horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
        return redirect(url_for('index'))
    else:
        return 'Ocorreu um erro ao adicionar o registro.'


@app.route('/editar/<int:registro_id>', methods=['GET', 'POST'])
def editar(registro_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form['data']
        horario = request.form['horario']
        nome_motorista = request.form['nome_motorista']
        cpf = request.form['cpf']
        placa = request.form['placa']
        nota_fiscal = request.form['nota_fiscal']
        itens = request.form['itens']
        fornecedor = request.form['fornecedor']
        destino = request.form['destino']
        horario_entrada = request.form['horario_entrada']
        horario_saida = request.form['horario_saida']
        porteiro = request.form['porteiro']
        entrada_saida = request.form['entrada_saida']
        natureza_operacao = request.form['natureza_operacao']

        if atualizar_registro(registro_id, data, horario, nome_motorista, cpf, placa, nota_fiscal, itens, fornecedor,
                              destino, horario_entrada, horario_saida, porteiro, entrada_saida, natureza_operacao):
            return redirect(url_for('index'))
        else:
            return 'Ocorreu um erro ao atualizar o registro.'
    else:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros WHERE id=?", (registro_id,))
        registro = cursor.fetchone()
        conn.close()
        return render_template('editar.html', registro=registro)


@app.route('/excluir/<int:registro_id>')
def excluir(registro_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if excluir_registro(registro_id):
        return redirect(url_for('index'))
    else:
        return 'Ocorreu um erro ao excluir o registro.'


if __name__ == '__main__':
    criar_tabela_registros()
    app.run(debug=True, host='192.168.2.4')