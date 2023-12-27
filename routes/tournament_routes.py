from flask import Blueprint, request, jsonify
from models import tournament, db, team
from datetime import datetime

tournament_bp = Blueprint('tournament_bp', __name__)

@tournament_bp.route('/tournament')
def GETListaTournament():
    Tournaments: list[tournament] = tournament.query.order_by(tournament.TournamentDate).all()


    TournamentSDTs = [{
        'id': Tournament.TournamentID,
        'name': Tournament.TournamentName,
        'date': Tournament.TournamentDate.isoformat()
    }for Tournament in Tournaments]
    
    return TournamentSDTs



@tournament_bp.route('/tournament/<id>')
def GETTournament(id):
    Tournament: tournament = tournament.query.get(id)
    
    TournamentSDT = {
        'id': Tournament.TournamentID,
        'name': Tournament.TournamentName,
        'date': Tournament.TournamentDate.isoformat(),
        'teams': [
            {
                'id': team.TeamID,
                'name': team.TeamName,
                'pokemons': [
                    Pokemon.ToJson('png')
                    for Pokemon in team.pokemon
                ]
            }
            for team in Tournament.team
        ]
    }
    
    return TournamentSDT



@tournament_bp.route('/tournament', methods=['POST'])
def POSTTournament():
    data = request.get_json()
    DataTorneio = datetime.fromisoformat(data['date'])
    
    if data['id']:
        New_Tournament: tournament = db.session.get(tournament, data['id'])
        New_Tournament.TournamentName = data['name']
        New_Tournament.TournamentDate = DataTorneio
    else:
        New_Tournament: tournament = tournament(
            TournamentName=data['name'],
            TournamentDate=DataTorneio
    )
    
    New_Tournament.team.clear()    
    for Team in data['teams']:
        New_Team = db.session.get(team, Team['id'])
        New_Tournament.team.append(New_Team)
    
    try:
        db.session.add(New_Tournament)
        db.session.commit()
        return jsonify({'message': 'Torneio salvo com sucesso.'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    
    finally:
        db.session.close()
        


@tournament_bp.route('/tournament/<id>', methods=['DELETE'])
def DELETETeam(id):
    delete_Tournament: tournament = db.session.get(tournament, id)
    
    try:
        db.session.delete(delete_Tournament)
        db.session.commit()
        return jsonify({'id': id,'message': 'Torneio deletado com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.session.close()