import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)

class StepsNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(10), nullable=False)

@app.route('/', methods=['GET'])
def index():
    # Fetching all step notes and reversing the order for display
    step_notes = StepsNote.query.order_by(StepsNote.id.desc()).all()
    # Calculating the total number of steps
    total_steps = sum(note.steps for note in step_notes) if step_notes else 0
    return flask.render_template('index.html', step_notes=step_notes, total_steps=total_steps)

@app.route('/add_step', methods=['POST'])
def add_step():
    try:
        steps = int(flask.request.form['step'])  
        date = flask.request.form['date']
        if steps > 0:
            new_step_note = StepsNote(steps=steps, date=date)
            db.session.add(new_step_note)
            db.session.commit()
        else:
            flask.flash('Number of steps must be greater than zero.')
    except ValueError:
        flask.flash('Please enter a valid number for steps.')
    return flask.redirect(flask.url_for('index'))

@app.route('/delete_all', methods=['GET'])
def delete_all():
    StepsNote.query.delete()
    db.session.commit()
    return flask.redirect(flask.url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
