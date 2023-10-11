from app import create_app, db
from flask_migrate import Migrate
from app.models import User

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }

if __name__ == '_main_':
    with app.app_context():
        db.create_all()
        app.run(debug=True)