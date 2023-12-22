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



TeamTournament = db.Table('TeamTournament',
    db.Column('TournamentID', db.Integer, db.ForeignKey('tournament.TournamentID'), primary_key=True),
    db.Column('TeamID', db.Integer, db.ForeignKey('team.TeamID'), primary_key=True)
)
class tournament(db.Model):
    TournamentID = db.Column(db.Integer, primary_key=True)
    TournamentName = db.Column(db.String(60), nullable=True)
    TournamentDate = db.Column(db.DateTime, nullable=True)
    team = db.relationship('team', secondary=TeamTournament, backref='tournament')
    
class team(db.Model):
    TeamID = db.Column(db.Integer, primary_key=True)
    TeamName = db.Column(db.String(60), nullable=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=True)
    pokemon = db.relationship('pokemon', secondary=TeamPokemon, backref='team')