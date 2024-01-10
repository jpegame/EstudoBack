from flask import Blueprint, request, jsonify
from models import tournament, db, team, match
from datetime import datetime
import random

tournament_bp = Blueprint('tournament_bp', __name__)

@tournament_bp.route('/tournament')
def GETListaTournament():
    
    Tournaments: list[tournament] = tournament.query.order_by(tournament.TournamentStartDate).all()
    TournamentSDTs = [{
        'id': Tournament.TournamentID,
        'name': Tournament.TournamentName,
        'start-date': Tournament.TournamentStartDate.isoformat(),
        'end-date': Tournament.TournamentEndDate.isoformat()
    }for Tournament in Tournaments]
    
    return TournamentSDTs



@tournament_bp.route('/tournament/<id>')
def GETTournament(id):
    Tournament: tournament = tournament.query.get(id)
    Matches: list(match) = match.query.filter_by(TournamentID=id).all()
    
    
    TournamentSDT = {
        'id': Tournament.TournamentID,
        'name': Tournament.TournamentName,
        'start-date': Tournament.TournamentStartDate.isoformat(),
        'end-date': Tournament.TournamentEndDate.isoformat(),
        'matches': [
            {
                'level': Match.MatchLevel,
                'status': Match.matchStatus,
                'team1':TeamFromMatch(Match.Team1ID),
                'team2':TeamFromMatch(Match.Team2ID),
            }
            for Match in Matches
        ]
    }
    
    return TournamentSDT



@tournament_bp.route('/tournament', methods=['POST'])
def POSTTournament():
    data = request.get_json()
    TournamentStartDate = datetime.fromisoformat(data['start-date'])
    TournamentEndDate = datetime.fromisoformat(data['end-date'])
    times = data['teams']
    
    if data['id']:
        New_Tournament: tournament = db.session.get(tournament, data['id'])
        New_Tournament.TournamentName = data['name']
        New_Tournament.TournamentStartDate = TournamentStartDate
        New_Tournament.TournamentEndDate = TournamentEndDate
        Matches: list(match) = match.query.filter_by(TournamentID=data['id']).all()
        
        for Match in Matches:
            db.session.delete(Match)
    else:
        New_Tournament: tournament = tournament(
            TournamentName=data['name'],
            TournamentStartDate=TournamentStartDate,
            TournamentEndDate=TournamentEndDate
    )
        
    db.session.add(New_Tournament)
    db.session.flush()
    db.session.refresh(New_Tournament)
    
    tournament_id = New_Tournament.TournamentID
        
    for _ in range(int(len(times)/2)):
        random_sample = random.sample(times, 2)
        
        New_Match = match(MatchLevel=0,TournamentID=tournament_id,Team1ID=random_sample[0],Team2ID=random_sample[1])
        db.session.add(New_Match)
        for value in random_sample:
            if value in times:
                times.remove(value)
    
    try:
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
    delete_matches: list(match) = match.query.filter_by(TournamentID=id).all()
    
    try:
        for delete_match in delete_matches:
            db.session.delete(delete_match)
            
        db.session.delete(delete_Tournament)
        db.session.commit()
        return jsonify({'id': id,'message': 'Torneio deletado com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.session.close()
        

def TeamFromMatch(teamid: int):
    Team: team = team.query.get(teamid)
    return {
        'id': Team.TeamID,
        'name': Team.TeamName,
        'pokemons': [
            Pokemon.ToJson('png')
            for Pokemon in Team.pokemon
        ]
    }