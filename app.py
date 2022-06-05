from flask import Flask
from flask import jsonify
from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image
import os

# GOOGLE_STORAGE_PROJECT = os.environ['GOOGLE_STORAGE_PROJECT']
# GOOGLE_STORAGE_BUCKET = os.environ['GOOGLE_STORAGE_BUCKET']

app = Flask(__name__)


NAME = ['Mad Girl', 'Depressed Girl', 'Heartbroken Girl', 'Possesed Girl']
RACE = ['White', 'African', 'Hispanic', 'Asian']

# DIFFICULTY =[
#     '7.2', '7.2', '8.5', '9.2'
# ]
# UNIQUE_STATS =[
#     '18 feet tall (27 foot wingspan), fly’s at normal speed, extreme strength',
#     '18 feet tall (27 foot wingspan), fly’s at normal speed, extreme strength',
#     '24 feet tall (35 foot wingspan), fly’s at high speed, extreme strength',
#     '30 feet tall (47 foot wingspan), fly’s at speed of sound, strongest dragon'
# ]

@app.route('/api/creature/<token_id>')
def creature(token_id):
    token_id = int(token_id)
    creature_name = NAME[token_id]
    image_url = _compose_image()

    attributes = []
    _add_attribute(attributes, 'RACE', RACE, token_id)
    # _add_attribute(attributes, 'DIFFICULTY', DIFFICULTY, token_id)
    # _add_attribute(attributes, 'UNIQUE STATS', UNIQUE_STATS, token_id)


    response = jsonify({
        'name': creature_name,
        'description': "demo",
        'image': image_url,
        'external_url': 'https://example.com/?token_id=%s' % token_id,
        'attributes': attributes
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/box/<token_id>')
def box(token_id):
    token_id = int(token_id)
    image_url = _compose_image()

    attributes = []
    _add_attribute(attributes, 'number_inside', [3], token_id)

    return jsonify({
        'name': "Creature Loot Box",
        'description': "This lootbox contains some OpenSea Creatures! It can also be traded!",
        'image': image_url,
        'external_url': 'https://example.com/?token_id=%s' % token_id,
        'attributes': attributes
    })


@app.route('/api/factory/<token_id>')
def factory(token_id):
    token_id = int(token_id)
    if token_id == 0:
        name = "One OpenSea creature"
        description = "When you purchase this option, you will receive a single OpenSea creature of a random variety. " \
                      "Enjoy and take good care of your aquatic being!"
        image_url = _compose_image(
            ['images/factory/egg.png'], token_id, "factory")
        num_inside = 1
    elif token_id == 1:
        name = "Four OpenSea creatures"
        description = "When you purchase this option, you will receive four OpenSea creatures of random variety. " \
                      "Enjoy and take good care of your aquatic beings!"
        image_url = _compose_image(
            ['images/factory/four-eggs.png'], token_id, "factory")
        num_inside = 4
    elif token_id == 2:
        name = "One OpenSea creature lootbox"
        description = "When you purchase this option, you will receive one lootbox, which can be opened to reveal three " \
                      "OpenSea creatures of random variety. Enjoy and take good care of these cute aquatic beings!"
        image_url = _compose_image(
            ['images/box/lootbox.png'], token_id, "factory")
        num_inside = 3

    attributes = []
    _add_attribute(attributes, 'number_inside', [num_inside], token_id)

    return jsonify({
        'name': name,
        'description': description,
        'image': image_url,
        'external_url': 'https://example.com/?token_id=%s' % token_id,
        'attributes': attributes
    })


def _add_attribute(existing, attribute_name, options, token_id, display_type=None):
    trait = {
        'trait_type': attribute_name,
        'value': options[token_id]
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)


def _compose_image():

   
    return "https://ipfs.io/ipfs/QmYgfNP82yqsWGC1jDVcB6WWUH5hR1QkEq3stahjUUrSJe"


# def _get_bucket():
#     credentials = service_account.Credentials.from_service_account_file(
#         'credentials/google-storage-credentials.json')
#     if credentials.requires_scopes:
#         credentials = credentials.with_scopes(
#             ['https://www.googleapis.com/auth/devstorage.read_write'])
#     client = storage.Client(
#         project=GOOGLE_STORAGE_PROJECT, credentials=credentials)
#     return client.get_bucket(GOOGLE_STORAGE_BUCKET)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
# test
# test
