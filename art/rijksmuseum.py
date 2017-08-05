from IPython.core.display import display, HTML, Image
import numpy as np
import requests
from urllib.parse import urljoin

class connect():
    def __init__(self, token, root_url="https://www.rijksmuseum.nl/api/en",
                 resource_url="collection"):
        self.url = urljoin(f"{root_url}/", f"{resource_url}")
        self.token = token
        
    def request(self, payload):
        req = requests.get(self.url, params=payload)   
        req.raise_for_status()
        return req.json()
        
    def get_item(self, keyword):
        payload = {}
        payload["key"] = self.token
        payload["format"] = "json"
        payload["q"] = keyword
        payload["imgonly"] = True
        payload["p"] = 0 # page number
        payload["ps"] = 50 # page size
        
        json_data = self.request(payload)
        if json_data["count"] == 0:
            raise Exception("No items found.")
        
        item_index = np.random.randint(json_data["count"])
        page_number = item_index // payload["ps"]
        page_index = item_index % payload["ps"]
        
        if page_number > 0:
            payload = {**payload, **{"page": page_number}}
            json_data = self.request(payload)
        
        item = json_data["artObjects"][page_index]
                
        return item

    def display_item(self, item):
        if item["permitDownload"]:
            req = requests.get(item["webImage"]["url"], stream="True")
            req.raise_for_status()
            image_data = req.raw.data
            display(Image(image_data))
        else:
            display(HTML("<i>This image is not available for download.</i>"))
        display(HTML("<b>Title:</b>"))
        display(HTML(item["longTitle"]))
    
    def send_me(self, keyword):
        item = self.get_item(keyword)
        self.display_item(item)
