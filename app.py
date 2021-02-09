from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


def herokudb():
    Host = 'ec2-18-203-62-227.eu-west-1.compute.amazonaws.com'
    Database = 'd493kefv8shc65'
    User = 'dyfepovpwicnty'
    Password = 'f7fa3c7a5ce9e03c2a7344173331c0db33d7370a90e4dc34cddb6c328aeeb178'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')


def gravar(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
    db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, code(v3)))
    ficheiro.commit()
    ficheiro.close()


def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor = None
    return valor


def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, code(v2),))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def alterar(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET passe = %s WHERE nome = %s", (code(v2), v1))
    ficheiro.commit()
    ficheiro.close()


def apaga(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE nome = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()

def code(passe):
    import hashlib
    return hashlib.sha3_256(passe.encode()).hexdigest()





def gravarinstr(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS instr (nome text, descri text, price text)")
    db.execute("INSERT INTO instr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def existeinstr(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM instr WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor=None
    return valor


def addinstr(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def alterarinstr(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("UPDATE instr SET price = %s WHERE nome = %s", (v2, v1))
    ficheiro.commit()
    ficheiro.close()


def apagainstr(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM instr WHERE nome = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()

def lista():
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM instr ORDER BY Nome DESC")
        valor = db.fetchall()
        ficheiro.close()
    except:
        valor = None
    return valor






@app.route('/registo', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['GET', 'POST'])
def apagar():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            apaga(v1)
            erro = 'Conta Eliminada com Sucesso.'
    return render_template('apagar.html', erro=erro)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v0 = request.form['apasse']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v0):
            erro = 'A palavra passe está errada.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
    return render_template('newpasse.html', erro=erro)





@app.route('/insinstr', methods=['GET', 'POST'])
def routeinstr():
    erro = None
    if request.method == 'POST':
        v1 = request.form['nome']
        v2 = request.form['descri']
        v3 = request.form['price']
        if existe(v1):
            erro = 'O Instrumento já existe.'
        else:
            gravar(v1, v2, v3)
            erro = 'Instrumento adicionado com sucesso.'
    return render_template('addinstr.html', erro=erro)

@app.route('/apagarintr', methods=['GET', 'POST'])
def apagarinstr():
    erro = None
    if request.method == 'POST':
        v1 = request.form['nome']
        if not existe(v1):
            erro = 'O Instrumento não existe.'
        else:
            apaga(v1)
            erro = 'Instrumento Eliminado com Sucesso.'
    return render_template('apagarinstr.html', erro=erro)

@app.route('/newprice', methods=['GET', 'POST'])
def newprice():
    erro = None
    if request.method == 'POST':
        v1 = request.form['nome']
        v2 = request.form['price']
        if not existe(v1):
            erro = 'O Instrumento não existe.'

        else:
            alterar(v1, v2)
            erro = 'Preço alterado com sucesso.'
    return render_template('altpreco.html', erro=erro)

@app.route('/search')
def search():
    dados = lista()
    return render_template('tableinst.html', tabela=dados, max=len(dados))





if __name__ == '__main__':
    app.run(debug=True)
