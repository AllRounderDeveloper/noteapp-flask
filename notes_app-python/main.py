# IMPORTS
from flask import Flask, render_template as rt, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# FLASK APP CONFIGURATION
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///note.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# MODEL
class Notes(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def ftime(self):
        return self.time.strftime("%d/%m/%Y - %H:%M:%S") if self.time else 'no time';

    def __repr__(self) -> str:
        return f"{self.sno}.{self.title} - {self.ftime}"

# CREATE TABLES BEFORE RUNNING THE APP
with app.app_context():
    db.create_all()

# END POINTS
# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    items = Notes.query.all()
    return rt('index.html', notes=items)

# add page
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        obj = Notes(title=title, desc=desc)
        db.session.add(obj)
        db.session.commit()

        return redirect(url_for('index'))

    return rt('add.html')

# delete endpoint
@app.route('/delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    if sno:
        item = Notes.query.filter_by(sno=sno).first()
        db.session.delete(item)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return 'Invalid sno'
    
#edit page
@app.route('/edit/<int:sno>', methods=["GET", "POST"])
def update(sno):
    item = Notes.query.filter_by(sno = sno).first()
    if request.method == "POST":
        item.title = request.form['title']
        item.desc = request.form['desc']
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    
    return rt('edit.html', note = item)

# RUNNING THE APP
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=80)
