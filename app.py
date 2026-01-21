from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Usuario, Lancamento

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segredo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
    
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = Usuario.query.filter_by(email=email, senha=senha).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    novo = Usuario(
        nome=request.form['nome'],
        email=request.form['email'],
        senha=request.form['senha']
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    lancamentos = Lancamento.query.filter_by(usuario_id=current_user.id).all()

    entradas = sum(l.valor for l in lancamentos if l.tipo == 'entrada')
    saidas = sum(l.valor for l in lancamentos if l.tipo == 'saida')
    saldo = entradas - saidas

    return render_template(
        'dashboard.html',
        entradas=entradas,
        saidas=saidas,
        saldo=saldo,
        lancamentos=lancamentos
    )


@app.route('/add', methods=['POST'])
@login_required
def add():
    novo = Lancamento(
        tipo=request.form['tipo'],
        categoria=request.form['categoria'],
        valor=float(request.form['valor']),
        usuario_id=current_user.id
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
