from flask import Blueprint
from models import pokemon
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
