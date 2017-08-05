from IPython.core.display import display, HTML, Image
import numpy as np
import requests
from urllib.parse import urljoin

class connect():
    def __init__(self, token, root_url="https://www.sfmoma.org/api/collection",
                 resource_url="artworks"):
        self.url = urljoin(f"{root_url}/", f"{resource_url}/")
        self.auth_header = {"Authorization": f"Token {token}"}
        
    def request(self, payload):
        req = requests.get(self.url, params=payload, headers=self.auth_header)   
        req.raise_for_status()
        return req.json()
        
    def get_item(self, keyword):
        payload = {}
        payload["object_keywords__regex"] = f"\m{keyword.lower()}\M"
        payload["page_size"] = 20
        payload["has_images"] = True
        
        json_data = self.request(payload)
        if json_data["count"] == 0:
            raise Exception("No items found.")
        
        item_index = np.random.randint(json_data["count"])
        page_number = item_index // payload["page_size"]
        page_number += 1 # first page has index 1 (not 0)
        page_index = item_index % payload["page_size"]
        
        if page_number > 1:
            payload = {**payload, **{"page": page_number}}
            json_data = self.request(payload)
        
        item = json_data["results"][page_index]
                
        return item

    def display_item(self, item):
        image = item["images"][0]
        display(Image(image["public_image"]))
        display(HTML("<b>Caption:</b>"))
        display(HTML(image["caption"]))
        display(HTML("<b>Keywords:</b>"))
        display(HTML(item["object_keywords"]))
    
    def send_me(self, keyword):
        item = self.get_item(keyword)
        self.display_item(item)
