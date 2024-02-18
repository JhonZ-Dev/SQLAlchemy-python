from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Definición del modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
# Ruta para mostrar la lista de usuarios
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
# Ruta para agregar un nuevo usuario
@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))
# Ruta para eliminar un usuario
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))
# Ruta para actualizar un usuario
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    user.username = request.form['new_username']

