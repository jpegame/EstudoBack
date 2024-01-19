from flask import Blueprint, session, request, jsonify
import hashlib
from sqlalchemy import or_
from models import match, team

match_bp = Blueprint('match_bp', __name__)

@match_bp.route('/matches')
def GETListaTournament():
    TeamUser: team = team.query.filter_by(UserID=session['userid']).first()
    
    Matches: list[match] = match.query.filter(or_(match.Team1ID==TeamUser.TeamID, match.Team2ID==TeamUser.TeamID)).all()
    
    RetornoJson = [{
        "id": Match.MatchID,
        "status": Match.matchStatus,
        "team1": get_team_name(Match.Team1ID),
        "team2": get_team_name(Match.Team2ID)
    }for Match in Matches]
    
    return RetornoJson
    
@match_bp.route('/hash', methods=['POST'])
def MatchHashRoom():
    data = request.get_json()
    
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data['message'].encode('utf-8'))
    hash_hex = sha256_hash.hexdigest()

    return jsonify({'hash':hash_hex}), 200
    
def get_team_name(id):
    Team = team.query.get(id)
    return Team.TeamName