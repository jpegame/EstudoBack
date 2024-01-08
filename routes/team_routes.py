from flask import Blueprint, request, jsonify
from models import team, db, pokemon
team_bp = Blueprint('team_bp', __name__)

@team_bp.route('/team')
def GETTeams():
    Teams: list(team) = team.query.all()
    
    TeamSDT = [{
        'id': Team.TeamID,
        'name': Team.TeamName,
        'user': Team.UserID,
        'pokemons': [
            Pokemon.ToJson('png')
            for Pokemon in Team.pokemon
        ]
    }for Team in Teams]
    
    return TeamSDT

@team_bp.route('/team/<id>')
def GETTeam(id):
    Team: team = team.query.get(id)
    
    TeamSDT = {
        'id': Team.TeamID,
        'name': Team.TeamName,
        'user': Team.UserID,
        'pokemons': [
            Pokemon.ToJson('png')
            for Pokemon in Team.pokemon
        ]
    }
    
    return TeamSDT

@team_bp.route('/teambyuser/<id>')
def GETTeamUser(id):
    Team: team = team.query.filter_by(UserID=int(id)).first()
    
    TeamSDT = {
        'id': Team.TeamID,
        'name': Team.TeamName,
        'user': Team.UserID,
        'pokemons': [
            Pokemon.ToJson('png')
            for Pokemon in Team.pokemon
        ]
    }
    
    return TeamSDT


@team_bp.route('/team', methods=['POST'])
def POSTTeam():
    data = request.get_json()
    
    if data['id']:
        New_Team: team = db.session.get(team, data['id'])
        New_Team.TeamName = data['name']
    else:
        New_Team: team = team(
            TeamName=data['name'],
            UserID=data['user']
        )
    
    New_Team.pokemon.clear()    
    for Pokemon in data['pokemons']:
        New_pokemon = db.session.get(pokemon, Pokemon['id'])
        New_Team.pokemon.append(New_pokemon)
    
    try:
        db.session.add(New_Team)
        db.session.commit()
        return jsonify({'id': New_Team.TeamID,'message': 'Time salvo com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.session.close()



@team_bp.route('/team/<id>', methods=['DELETE'])
def DELETETeam(id):
    delete_Team: team = db.session.get(team, id)
    
    try:
        db.session.delete(delete_Team)
        db.session.commit()
        return jsonify({'id': id,'message': 'Time deletado com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.session.close()
    
    