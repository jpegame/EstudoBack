from flask import Flask
from flask_cors import CORS
from routes.index_routes import index_bp
from routes.pokemon_routes import pokemon_bp
from routes.login_routes import login_bp
from routes.team_routes import team_bp
from routes.tournament_routes import tournament_bp
from models import db

app = Flask(__name__)
app.secret_key = '8d5871ce-00ea-4e93-a1f1-e4b3d81d032d'
CORS(app, supports_credentials=True)#supports_credentials=True

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
app.register_blueprint(login_bp)
app.register_blueprint(team_bp)
app.register_blueprint(tournament_bp)

if __name__ == '__main__':
    app.run(debug=True,port=3001)
