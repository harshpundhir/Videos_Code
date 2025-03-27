import requests
from pprint import pprint
'''
https://api.iconify.design
https://api.simplesvg.com
https://api.unisvg.com
'''
class InconifyAPI:
    def __init__(self, url):
        self.url = url

    def get_icon(self, prefix, name):
        response = requests.get(f"{self.url}/{prefix}/{name}")
        return response.text
    
    def search_icon(self, query, limit=5):
        response = requests.get(f"{self.url}/search?query={query}&limit={limit}")
        return dict(response.json()).get("icons", [])
    
    def search_and_get_icon(self, search_query):
        raise NotImplementedError
    
api = InconifyAPI("https://api.iconify.design")
icon = api.search_icon("alarm")
pprint(icon)
svg = (api.get_icon(*["fluent-emoji-flat","alarm-clock.svg"]))
with open("temp.svg", "w") as f:
    f.write(svg)