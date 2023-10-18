from app import create_app, db
from app.Model.models import Position, Research_field, Language

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'Position': Position, 'User': User}

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
        if Research_field.query.count() == 0:
            fields = ['Machine Learning','High Performance Computing', 'Quantum Computing']
            for f in fields:
                db.session.add(Research_field(name=f))
            db.session.commit()
        if Language.query.count() == 0:
            languages = ['Python','C++', 'Javascript', 'CSS', 'HTML']
            for l in languages:
                db.session.add(Language(name=l))
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)