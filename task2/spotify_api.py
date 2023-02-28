"""
Based on the provided artist name only (ACDC)
the following fields are accessible in the
json object: artist name, most popular song,
artist ID, and country (available_markets)
of the most popular song.
"""

import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

AUTH_URL = 'https://accounts.spotify.com/api/token'
coded_credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()


def main(credentials, url, name):
    """
    Main module to render required data
    >>> main(coded_credentials, AUTH_URL, 'Imagine Dragons')
    Artist name: Imagine Dragons\n\
    Most popular song: Believer\n\
    Artist id: 53XhwfbYqKCa1cC15pYq2q\n\
    Country: UA
    >>> main(11, 11, 11)
    'Wrong data type'
    """
    for inpt in [credentials, url, name]:
        if not isinstance(inpt, str):
            return 'Wrong data type'

    out = get_data(credentials, url, name)
    print(f'Artist name: {out[0]}')
    print(f'Most popular song: {out[1]}')
    print(f'Artist id: {out[2]}')
    print(f'Country: {out[3]}')


def get_data(credentials, url, name):
    """
    Module to send get requests and receive data
    """
    auth_data = {'grant_type': 'client_credentials'}
    auth_headers = {'Authorization': f'Basic {credentials}'}
    response = requests.post(url, data = auth_data, headers = auth_headers)
    access_token = response.json().get('access_token')
    base_url = 'https://api.spotify.com/v1/search/'
    request_params = {
        'query': name,
        'type': 'artist'
    }
    request_headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(base_url, headers = request_headers, params=request_params)
    response_data = response.json()

    # artist name and id
    artist_name, artist_id = artist_name_id(response_data)[0], artist_name_id(response_data)[1]

    # get most popular song and country
    # to get all countries
    # markets = requests.get("https://api.spotify.com/v1/markets", headers = request_headers).json()
    song=sorted(requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UA"
    ,headers=request_headers,timeout=1).json()["tracks"], key=lambda x: x["popularity"])[-1]["name"]

    return artist_name, song, artist_id, "UA"


def artist_name_id(data):
    """
    Module to sort data received by get_data module
    """
    sond_popularity = []

    # search most popular song
    for entry in data['artists']["items"]:
        sond_popularity.append((entry['name'], entry['popularity'], entry['id']))
    sorted_data = sorted(sond_popularity, key=lambda x: x[1])
    most_popular_artist = sorted_data[-1][0]
    artist_id = sorted_data[-1][-1]

    return most_popular_artist, artist_id


if __name__ == '__main__':
    main(coded_credentials, AUTH_URL, 'Imagine Dragons')
    import doctest
    print(doctest.testmod())
