from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Pokemon_Type = db.Table('Pokemon_Type',
    db.Column('PokemonID', db.Integer, db.ForeignKey('pokemon.PokemonID'), primary_key=True),
    db.Column('TypeID', db.Integer, db.ForeignKey('type.TypeID'), primary_key=True)
)

TeamPokemon = db.Table('TeamPokemon',
    db.Column('PokemonID', db.Integer, db.ForeignKey('pokemon.PokemonID'), primary_key=True),
    db.Column('TeamID', db.Integer, db.ForeignKey('team.TeamID'), primary_key=True)
)


class pokemon(db.Model):
    PokemonID = db.Column(db.Integer, primary_key=True)
    PokemonName = db.Column(db.String(60), nullable=True)
    PokemonImage = db.Column(db.String(100), nullable=True)
    PokemonRaridade = db.Column(db.String(1), nullable=True)
    type = db.relationship('type', secondary=Pokemon_Type, backref='pokemon')
    
    def ToJson(self,TipoImagem):
        return {
            'id': self.PokemonID,
            'name': self.PokemonName,
            'image': self.PokemonImage if TipoImagem == 'gif' else 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/' + str(self.PokemonID) + '.png',
            'rarity': self.PokemonRaridade,
            'type': [
                tipo.TypeDescription
                for tipo in self.type
            ]
        }

class user(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(40), unique=True)
    Password = db.Column(db.String(40))

class type(db.Model):
    TypeID = db.Column(db.Integer, primary_key=True)
    TypeDescription = db.Column(db.String(40), unique=True)

class match(db.Model):
    MatchID = db.Column(db.Integer, primary_key=True)
    matchStatus = db.Column(db.Enum('AGENDADA', 'EM ANDAMENTO','FINALIZADA', name='status_enum'), server_default='AGENDADA', nullable=True)
    MatchLevel = db.Column(db.Integer, nullable=True)
    TournamentID = db.Column(db.Integer, db.ForeignKey('tournament.TournamentID'), nullable=True)
    Team1ID = db.Column(db.Integer, db.ForeignKey('team.TeamID'), nullable=True)
    Team2ID = db.Column(db.Integer, db.ForeignKey('team.TeamID'), nullable=True)

class tournament(db.Model):
    TournamentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TournamentName = db.Column(db.String(60), nullable=True)
    TournamentStartDate = db.Column(db.DateTime, nullable=True)
    TournamentEndDate = db.Column(db.DateTime, nullable=True)

class team(db.Model):
    TeamID = db.Column(db.Integer, primary_key=True)
    TeamName = db.Column(db.String(60), nullable=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=True)
    pokemon = db.relationship('pokemon', secondary=TeamPokemon, backref='team')