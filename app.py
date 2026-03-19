import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# МОДЕЛЬ ДАННЫХ
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)

# Создаем базу данных прямо при запуске
with app.app_context():
    db.create_all()

# МАРШРУТЫ

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form.get('name')
        if user_name:
            # Сохраняем имя в базу данных
            new_visit = Visit(username=user_name)
            db.session.add(new_visit)
            db.session.commit()
            return redirect(url_for('index'))
    
    # Получаем список всех, кто заходил
    all_visits = Visit.query.order_by(Visit.visit_time.desc()).all()
    return render_template("index.html", visits=all_visits)

if __name__ == "__main__":
    app.run(debug=True)

