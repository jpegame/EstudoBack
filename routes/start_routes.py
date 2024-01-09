from flask import request
from flask_socketio import SocketIO
import json

socketio = SocketIO()

@socketio.on('user_ready')
def handle_user_ready(data):
    user_id = data['user_id']
    print(f"User {user_id} is ready!")

    if user_id == 1:
        socketio.emit('user1_ready' + data['salaid'])
    elif user_id == 2:
        socketio.emit('user2_ready' + data['salaid'])


SalaSelected = []
@socketio.on('pokemon_selected')
def handle_user_ready(data):
    global SalaSelected
    Emit = False
    
    print(SalaSelected)
    for i in SalaSelected:
        if data['salaid'] in i['sala']:
            retorno = [{
                'pokemon': data['pokemon'],
                'userid': data['userid']
            },{
                'pokemon': i['pokemon'],
                'userid': i['userid']
            }]
            
            socketio.emit('pokemonbothselected' + data['salaid'], json.dumps(retorno))  
            SalaSelected.remove(i)
            Emit = True
            
    if not Emit:
        SalaSelected.append({'sala':data['salaid'],'pokemon': data['pokemon'], 'userid': data['userid']})
    
# client_turns = {}
# @socketio.on('turn_taken')
# def handle_turn_taken():
#     print(request.sid)
#     client_turns[request.sid] = 3 - client_turns[request.sid]
#     socketio.emit('update_turn', {'turn': client_turns[request.sid]}, broadcast=True)
    
    
@socketio.on('take_damage')
def handle_turn_taken(data):
    socketio.emit('update_life' + data['salaid'], data)