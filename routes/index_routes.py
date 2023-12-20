from flask import Blueprint, render_template
from models import pokemon
index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    Pokemons = pokemon.query.all()

    PokemonSDT = [
        {
            'id': Pokemon.PokemonID,
            'name': Pokemon.PokemonName,
            'image': Pokemon.PokemonImage,
            'rarity': Pokemon.PokemonRaridade
        }
        for Pokemon in Pokemons
    ]

    return render_template('index.html', pokemons=PokemonSDT)

@index_bp.route('/<id>')
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
    return render_template('pokemon.html', pokemon=PokemonSDT)
