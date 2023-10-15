from app import create_app, db
from app.Model.models import Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'Post': Post, 'User': User}

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)