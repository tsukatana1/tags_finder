import requests
import os
import helpers
from dotenv import load_dotenv

load_dotenv()

#API URL's
YOUTUBE_URL = "https://youtube.googleapis.com/youtube/v3"
INSTAGRAM_URL = "https://graph.facebook.com/"
PINTEREST_URL = "https://api-sandbox.pinterest.com/v5"

#API tokens
YT_KEY = os.getenv("YT_API_KEY")
PIN_KEY = os.getenv("PIN_KEY")

#Cache for storing past results
cache = {}

"""
YouTube functions:

    request_youtube:
        calls extract_ids (wrapper function to make it cleaner)
    extract_ids:
        calls search endpoint to find x amount of most popular videos based on a query 
    get_tags:
        calls video endpoint to find information about each video ID provided by extract_ids

Dashboard: https://console.cloud.google.com/apis/
"""
def request_youtube(query: str, **kwargs) -> list:
    if kwargs.get('max_results') is None:
        max_res = 5
    else: 
        max_res = kwargs['max_results']

    if cache.get(query) is not None:
        print(f"in cache: {cache[query]}")
        return cache[query]

    tags = get_tags(query, max_res)
    result = helpers.calculate_freq(tags)
    cache[query] = result
    return result

def extract_ids(query: str, max_res: int) -> list:
    ids = []
    format_url = f"{YOUTUBE_URL}/search?part=snippet&maxResults={max_res}&order=viewCount&q={query}&type=video&key={YT_KEY}"
    res = requests.get(format_url, headers = {'Accept': 'application/json'})
    r = res.json()

    for i in r.get("items"):
        ids.append(i.get("id").get("videoId"))

    return ids


def get_tags(query: str, max_res: int) -> list:
    tags = []
    ids = extract_ids(query, max_res)
    format_id = "%2C".join(ids)
    format_url = f"{YOUTUBE_URL}/videos?part=snippet&id={format_id}&key={YT_KEY}"
    res = requests.get(format_url, headers={"Accept": "application/json"})
    r = res.json()

    for i in r.get("items"):
        if i.get("snippet").get("tags") is not None:
            tags.append(i.get("snippet").get("tags"))

    return tags

"""
Pinterest functions:

    request_pinterest:
        calls term search endpoint to find most searched related words to the query

Dashboard: https://developers.pinterest.com/
NOTE: as of now, pinterest is not supported. a pause will be taken in this project,
due to the stupidity of these API's.
"""
def request_pinterest(query: str) -> dict:
    format_url = f"{PINTEREST_URL}/terms/suggested?term={query}"
    res = requests.get(format_url, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer: {PIN_KEY}'})
    r = res.json()

    return r
