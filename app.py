# app.py
from flask import Flask
from flask_cors import CORS
from routes.index_routes import index_bp
from routes.pokemon_routes import pokemon_bp
from models import db

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0@localhost/flask_estudo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables if they do not exist
with app.app_context():
    db.create_all()

# BluePrints
app.register_blueprint(index_bp)
app.register_blueprint(pokemon_bp)

if __name__ == '__main__':
    app.run(debug=True)
