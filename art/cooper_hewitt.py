from IPython.core.display import display, HTML, Image
import numpy as np
import requests
from urllib.parse import urljoin

class connect():
    def __init__(self, token, root_url="https://api.collection.cooperhewitt.org",
                 resource_url="rest"):
        self.url = urljoin(f"{root_url}/", f"{resource_url}/")
        self.token = token
        
    def request(self, payload):
        req = requests.get(self.url, params=payload)   
        req.raise_for_status()
        return req.json()
        
    def get_item(self, keyword):
        payload = {}
        payload["method"] = "cooperhewitt.search.objects"
        payload["access_token"] = self.token
        payload["has_images"] = 1
        payload["tag"] = keyword
        payload["page"] = 1
        payload["per_page"] = 50
        
        json_data = self.request(payload)
        if json_data["total"] == 0:
            raise Exception("No items found.")
        
        item_index = np.random.randint(json_data["total"])
        page_number = item_index // payload["per_page"]
        page_number += 1 # first page has index 1 (not 0)
        page_index = item_index % payload["per_page"]
        
        if page_number > 1:
            payload = {**payload, **{"page": page_number}}
            json_data = self.request(payload)
        
        item = json_data["objects"][page_index]
                
        return item

    def display_item(self, item):
        image = item["images"][0]
        image = image["z"] # 640px on the longest side]
        display(Image(image["url"]))       
        display(HTML("<b>Description:</b>"))
        display(HTML(item["description"]))
        for person in item["participants"]:
            role_name = person["role_name"]
            person_name = person["person_name"]
            display(HTML(f"<i>{role_name}</i>: {person_name}"))         
    
    def send_me(self, keyword):
        item = self.get_item(keyword)
        self.display_item(item)
