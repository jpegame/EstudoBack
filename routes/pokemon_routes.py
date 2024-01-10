from flask import Blueprint, request, jsonify
from models import pokemon
from random import sample
import requests

pokemon_bp = Blueprint('pokemon_bp', __name__)

@pokemon_bp.route('/pokemon')
def index():
    Pokemons = pokemon.query.order_by(pokemon.PokemonID).all()

    PokemonSDTs = [
        Pokemon.ToJson('gif')
        for Pokemon in Pokemons
    ]

    return PokemonSDTs

@pokemon_bp.route('/pokemon/<id>')
def index_single(id):
    Pokemon = pokemon.query.get(id)

    if Pokemon is None:
        return "<p>Pokemon não existe!</p>"

    return Pokemon.ToJson('png')

class Move():
    def __init__(self, url):
        req = requests.get(url)
        self.json = req.json()
        self.name = self.json['name']
        self.power = self.json['power']
        self.type = self.json['type']['name']
        self.pp = self.json['pp']
    def Json(self):
        return {
            'name': self.name,
            'power': self.power,
            'type': self.type,
            'pp':self.pp
        }

@pokemon_bp.route('/pokemon-stats')
def pokemonstats():
    id  = request.args.get('id', None)
    level  = int(request.args.get('level', 0))
    
    if id and level:
        response = requests.get('https://pokeapi.co/api/v2/pokemon/' + id)

        if response.status_code == 200:
            pokemon_data = response.json()
            moves = {
                'id':id,
                'name':pokemon_data['forms'][0]['name'],
                'hp':pokemon_data['stats'][0]['base_stat'] + level,
                'attack':pokemon_data['stats'][1]['base_stat'] + level,
                'defense':pokemon_data['stats'][2]['base_stat'] + level,
                'moves':[]
            }

            for move in pokemon_data['moves']:
                for version in move['version_group_details']:
                    if version['version_group']['name'] == 'red-blue' and version['move_learn_method']['name'] == 'level-up':
                        if level >= version['level_learned_at']:
                            move_pokemon = Move(move['move']['url'])
                            print(move['move']['url'])
                            moveDict = move_pokemon.Json()
                            if moveDict not in moves['moves'] and move_pokemon.power is not None:        
                                moves['moves'].append(moveDict)
                                    
            if len(moves['moves']) > 4:
                moves['moves'] = sample(moves['moves'], 4)
            
            return moves
        
        return jsonify({'message': 'Pokemon not found'}), response.status_code


