from flask import Blueprint
from models import pokemon
pokemon_bp = Blueprint('pokemon_bp', __name__)

@pokemon_bp.route('/pokemon')
def index():
    Pokemons = pokemon.query.all()

    PokemonSDTs = [
        {
            'id': Pokemon.PokemonID,
            'name': Pokemon.PokemonName,
            'image': Pokemon.PokemonImage,
            'rarity': Pokemon.PokemonRaridade
        }
        for Pokemon in Pokemons
    ]

    return PokemonSDTs

@pokemon_bp.route('/pokemon/<id>')
def index_single(id):
    Pokemon = pokemon.query.get(id)

    if Pokemon is None:
        return "<p>Pokemon não existe!</p>"

    PokemonSDT = {
        'id': Pokemon.PokemonID,
        'name': Pokemon.PokemonName,
        'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/' + str(Pokemon.PokemonID) + '.png',
        'rarity': Pokemon.PokemonRaridade,
        'type': [
            tipo.TypeDescription
            for tipo in Pokemon.type
        ]
    }
    return PokemonSDT
