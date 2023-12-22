from flask import Blueprint, session, request, jsonify
from models import user,db
login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    UserLogged = user.query.filter_by(UserName=data['username'],Password=data['password']).first()
    
    if UserLogged:
        session['logged_in'] = True
        session['username'] = UserLogged.UserID
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


    
@login_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'}), 200



@login_bp.route('/register', methods=['POST'])
def register():
    try:   
        data = request.get_json()
        NewUser = user(UserName=data['username'],Password=data['password'])
        db.session.add(NewUser)
        db.session.commit()
        return jsonify({'message': 'User saved successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        error_message = {'message': f'Error: {str(e)}'}
        return jsonify(error_message), 500
    finally:
        db.session.close()
        


@login_bp.route('/user_info')
def user_info():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({'username': session['username']}), 200
    else:
        return jsonify({'message': 'Not logged in'}), 401
        
        