import os
from app import create_app, db
from app.models import User
from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

if __name__ == "__main__":
	manager.run()
