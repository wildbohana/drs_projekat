from Configuration.config import app, db
from Routes.__init__ import *
from Models.User import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
